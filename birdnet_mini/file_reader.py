import glob
from pathlib import Path
from threading import Thread

from audio import open_audio_file, split_signal


class FileReader(Thread):

    def __init__(self, path, sample_rate, sample_queue, file_part_size_sec=60):
        super(FileReader, self).__init__()
        self._files = glob.glob(str(Path(path) / "*.wav"))
        self._sample_rate = sample_rate
        self._sample_queue = sample_queue
        self._file_part_size_sec = file_part_size_sec

        # use fixed values for chunk size and overlap
        self._chunk_size = 3.0
        self._overlap = 0
        self._min_len = 1.0

        self._interrupted = False

    def interrupt(self):
        self._interrupted = True

    def run(self):
        for file in self._files:
            # since we know that our audio is 5min max - load it at once
            sig, rate = open_audio_file(file, self._sample_rate)
            chunks = split_signal(sig, rate, self._chunk_size, self._overlap, self._min_len)
            for chunk_idx, chunk in enumerate(chunks):
                self._sample_queue.put(chunk)
        print("[filereader] Finished reading all files")

