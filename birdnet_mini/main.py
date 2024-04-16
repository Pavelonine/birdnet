import sys
import argparse
import time
from pathlib import Path
from queue import Queue

from birdnet_mini.model import Model
from birdnet_mini.file_reader import FileReader
from birdnet_mini.classifier import BirdClassifier
from birdnet_mini.transmission import SerialSender

SCRIPT_DIR = Path(__file__).resolve().parent
AUDIO_FOLDER_PATH = SCRIPT_DIR / "k:" / "science-camp" / "Data"
METADATA_FILE_PATH = SCRIPT_DIR / "k:" / "science-camp" / "SMM11597_Summary.txt"
MODEL_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Model_FP32.tflite"
LABELS_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Labels.txt"


def main():

    sample_queue = Queue()
    result_queue = Queue()

    with open(LABELS_FILE_PATH, "r") as f:
        labels = f.read().splitlines()

    model = Model(MODEL_FILE_PATH, labels)

    # Create the file_reader, classifier, and serial_sender objects
    file_reader = FileReader(AUDIO_FOLDER_PATH, METADATA_FILE_PATH, 48000, sample_queue)
    classifier = BirdClassifier(model, sample_queue, result_queue)
    serial_sender = SerialSender(result_queue, "COM4")

    # Start the threads
    serial_sender.start()
    classifier.start()
    file_reader.start()

    # enter main loop
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("[main ] Externally interrupted. Stopping threads.")
        file_reader.interrupt()
        classifier.interrupt()
        serial_sender.interrupt()

    file_reader.join()
    classifier.join()
    serial_sender.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BirdNet Mini")
    sys.exit(main())
