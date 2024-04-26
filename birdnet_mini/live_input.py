import numpy as np
import pyaudio

import datetime
from threading import Thread


class LiveMicrophoneInput(Thread):

    def __init__(self, device_index, sample_rate, sample_queue, lat=None, lon=None):
        super(LiveMicrophoneInput, self).__init__()
        self._sample_rate = sample_rate
        self._sample_queue = sample_queue
        self._device_index = device_index
        self._lat = lat
        self._lon = lon

        self._pa = pyaudio.PyAudio()

        candidate_name_parts = ["tlv320"]
        candidate_names = {}
        candidate_device_index = device_index
        info = self._pa.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')

        for i in range(0, num_devices):
            dev_info = self._pa.get_device_info_by_host_api_device_index(0, i)
            if (dev_info.get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", dev_info.get('name'))
                candidate_names[i] = dev_info.get('name')
                for candidat_name_part in candidate_name_parts:
                    if candidat_name_part in dev_info.get('name'):
                        candidate_device_index = i
                        break

        if device_index is None or device_index not in candidate_names.keys():
            print(f"Invalid device index - Using device with index {candidate_device_index} "
                  f"({candidate_names[candidate_device_index]})")
            self._device_index = candidate_device_index
        else:
            if device_index != candidate_device_index:
                print(f"Using device index {device_index} ({candidate_names[device_index]}) instead of expected "
                      f"{candidate_device_index} ({candidate_names[candidate_device_index]})")
            self._device_index = device_index

        # use fixed values for chunk size and overlap
        self._chunk_size = 3.0
        self._overlap = 0
        self._min_len = 1.0

        self._interrupted = False

    def interrupt(self):
        self._interrupted = True

    def run(self):

        stream = self._pa.open(format=pyaudio.paFloat32,
                               channels=1,
                               rate=self._sample_rate,
                               input=True,
                               frames_per_buffer=int(self._sample_rate * self._chunk_size),
                               input_device_index=self._device_index)

        while not self._interrupted:
            data = stream.read(int(self._sample_rate * self._chunk_size))
            chunk = np.frombuffer(data, 'float32')
            chunk_ts = datetime.datetime.now()
            self._sample_queue.put((chunk, chunk_ts, self._lat, self._lon))

        stream.stop_stream()
        stream.close()
        self._pa.terminate()

    @staticmethod
    def list_devices():
        pa = pyaudio.PyAudio()
        info = pa.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(0, num_devices):
            dev_info = pa.get_device_info_by_host_api_device_index(0, i)
            if (dev_info.get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", dev_info.get('name'))
        pa.terminate()
