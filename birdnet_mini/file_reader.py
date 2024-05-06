import glob
import os.path
import time
import datetime
from pathlib import Path
from threading import Thread

from birdnet_mini.audio import open_audio_file, split_signal
from birdnet_mini.metadata import MetaData


class FileReader(Thread):

    def __init__(self, path, metadata_file, sample_rate, sample_queue,  latitude, longitude, simulation_time=2.0):
        super(FileReader, self).__init__()
        self._files = glob.glob(str(Path(path) / "*.wav"))
        if metadata_file is None or not os.path.exists(metadata_file):
            self._metadata = None
            self._latitude = latitude
            self._longitude = longitude
        else:
            self._metadata = MetaData(metadata_file)
        self._sample_rate = sample_rate
        self._sample_queue = sample_queue

        # use fixed values for chunk size and overlap
        self._chunk_size = 3.0
        self._overlap = 0
        self._min_len = 1.0
        self._simulation_time = simulation_time

        self._interrupted = False

    def interrupt(self):
        self._interrupted = True

    def run(self):
        for file in self._files:
            if self._metadata is None:
                file_ts = datetime.datetime.now()
                file_lat = self._latitude
                file_lon = self._longitude
            else:
                file_ts, file_lat, file_lon = self._metadata.get_timestamp_lat_lon(str(Path(file).stem))

            if self._interrupted:
                break
            if file_ts is None or file_lat is None or file_lon is None:
                print(f"[filereader] Skipping file {file} - no metadata found")
                continue
            print(f"[filereader] Loading file {file}")
            # since we know that our audio is 5min max - load it at once
            sig, rate = open_audio_file(file, self._sample_rate)
            chunks = split_signal(sig, rate, self._chunk_size, self._overlap, self._min_len)
            for chunk_idx, chunk in enumerate(chunks):
                if self._interrupted:
                    break
                chunk_ts = file_ts + datetime.timedelta(seconds=chunk_idx * self._chunk_size)
                time.sleep(self._simulation_time)  # simulate processing time
                self._sample_queue.put((chunk, chunk_ts, file_lat, file_lon))
        if self._interrupted:
            print("[filereader] Interrupted")
        else:
            print("[filereader] Finished reading all files")

