import json
import os.path
import queue
import time
import struct
from threading import Thread

import serial

FIXED_MESSAGE_LENGTH = 24


class ResultWriter(Thread):
    def __init__(self, result_queue, target_folder, target_file_base="birdnet_results", max_entries=1000,
                 update_file_interval=100):
        super(ResultWriter, self).__init__()
        self._result_queue = result_queue
        self._target_folder = target_folder
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        self._target_file_base = target_file_base
        self._max_entries = max_entries
        self._update_file_interval = update_file_interval
        self._interrupted = False

    def interrupt(self):
        self._interrupted = True

    def run(self):
        file_entries = []
        file_counter = 0
        target_filename = f"{self._target_file_base}_{file_counter:05d}.json"
        while not self._interrupted:
            try:
                data_dict = self._result_queue.get(timeout=0.05)
            except queue.Empty:
                continue
            data_dict["timestamp"] = float(data_dict["timestamp"].timestamp())
            file_entries.append(data_dict)
            if len(file_entries) % self._update_file_interval == 0 or len(file_entries) >= self._max_entries:
                print(f"[result_writer] Writing {len(file_entries)} entries to {target_filename}")
                target_path = os.path.join(self._target_folder, target_filename)
                with open(target_path, "w") as fh:
                    fh.write(json.dumps(file_entries, indent=2))

            if len(file_entries) >= self._max_entries:
                file_entries = []
                file_counter += 1
                target_filename = f"{self._target_file_base}_{file_counter:05d}.json"

        with open(target_filename, "w") as fh:
            fh.write(json.dumps(file_entries))
