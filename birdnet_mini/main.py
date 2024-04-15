import sys
import argparse
import time
from pathlib import Path
from queue import Queue

from birdnet_mini.file_reader import FileReader
from birdnet_mini.classifier import BirdClassifier
from birdnet_mini.transmission import SerialSender

SCRIPT_DIR = Path(__file__).resolve().parent
TEST_FILE_PATH = SCRIPT_DIR / ".." / "testdata" / "test.wav"


def main():

    sample_queue = Queue(maxsize=100)
    result_queue = Queue()

    # create the file reader
    file_reader = FileReader(TEST_FILE_PATH.parent, 48000, sample_queue)

    # create the classifier
    classifier = BirdClassifier(sample_queue, result_queue)

    # create the sender
    serial_sender = SerialSender(result_queue, "COM4")

    file_reader.start()
    classifier.start()
    serial_sender.start()

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("[main] Interrupted by user")

    serial_sender.interrupt()
    file_reader.interrupt()
    classifier.interrupt()

    file_reader.join()
    classifier.join()
    serial_sender.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BirdNet Mini")
    sys.exit(main())
