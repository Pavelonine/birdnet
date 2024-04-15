import queue
import time
import struct
from threading import Thread

import serial

FIXED_MESSAGE_LENGTH = 24


class SerialSender (Thread):
    def __init__(self,  result_queue, serial_port, serial_rate=115200, send_interval_sec=2):
        super(SerialSender, self).__init__()
        self._serial_port = serial_port
        self._result_queue = result_queue
        self._serial = serial.Serial(serial_port, serial_rate, timeout=1)
        self._interrupted = False
        self.send_interval = send_interval_sec

    def interrupt(self):
        self._interrupted = True

    def run(self):
        while not self._interrupted:
            try:
                data_dict = self._result_queue.get(timeout=0.1)
            except queue.Empty:
                print(f"[serial] No data in queue")
                continue

            data_simple = [data_dict['class_id'], data_dict['confidence'],
                           data_dict['lat'], data_dict['lon'], data_dict['timestamp']]

            print(f"[serial] sending result data : {data_simple}")

            binary_data_struct = struct.pack('Hfffd', *data_simple)

            if len(binary_data_struct) != FIXED_MESSAGE_LENGTH:
                print(f"[serial] Error: Message size does not match: {len(binary_data_struct)} <> {FIXED_MESSAGE_LENGTH} bytes")
            else:
                self._serial.write(binary_data_struct)
            time.sleep(self.send_interval)

        self._serial.close()
