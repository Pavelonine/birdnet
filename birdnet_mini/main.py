import sys
import argparse
import time
from pathlib import Path
from queue import Queue

from birdnet_mini.live_input import LiveMicrophoneInput
from birdnet_mini.model import Model
from birdnet_mini.file_reader import FileReader
from birdnet_mini.classifier import BirdClassifier
from birdnet_mini.transmission import SerialSender

SCRIPT_DIR = Path(__file__).resolve().parent


def main(args):

    sample_queue = Queue()
    result_queue = Queue()

    with open(args.labels_file, "r") as f:
        labels = f.read().splitlines()

    model = Model(args.model_file, labels)

    # Create the file_reader, classifier, and serial_sender objects1
    if args.live:
        input = LiveMicrophoneInput(0, 48000, sample_queue, args.latitude, args.longitude)
    else:
        input = FileReader(args.audio_folder, args.metadata_file, 48000, sample_queue)
    classifier = BirdClassifier(model, sample_queue, result_queue)
    serial_sender = SerialSender(result_queue, args.serial_port)

    # Start the threads
    serial_sender.start()
    classifier.start()
    input.start()

    # enter main loop
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("[main ] Externally interrupted. Stopping threads.")
        input.interrupt()
        classifier.interrupt()
        serial_sender.interrupt()

    input.join()
    classifier.join()
    serial_sender.join()


if __name__ == "__main__":

    AUDIO_FOLDER_PATH = Path("k:") / "science-camp" / "Data"
    METADATA_FILE_PATH = Path("k:") / "science-camp" / "SMM11597_Summary.txt"
    MODEL_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Model_FP32.tflite"
    LABELS_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Labels.txt"

    parser = argparse.ArgumentParser(description="BirdNet Mini")

    parser.add_argument("--audio-folder", type=str, default=AUDIO_FOLDER_PATH,
                        help="Path to the audio folder.")
    parser.add_argument("--metadata_file", type=str, default=METADATA_FILE_PATH,
                        help="Path to the metadata file.")
    parser.add_argument("--model-file", type=str, default=MODEL_FILE_PATH,
                        help="Path to the model file.")
    parser.add_argument("--labels-file", type=str, default=LABELS_FILE_PATH,
                        help="Path to the labels file.")
    parser.add_argument("--serial-port", type=str, default=None,
                        help="Serial port to be used for IoT transmission")
    parser.add_argument("--live", action="store_true",
                        help="Use live microphone input instead of file input.")
    parser.add_argument("--latitude", type=float, default=50.68337,
                        help="Latitude of the recording location. Only used for live input.")
    parser.add_argument("--longitude", type=float, default=10.93209,
                        help="Longitude of the recording location. Only used for live input.")
    parser.add_argument("--list-devices",  action="store_true",
                        help="List available audio devices.")
    parser.add_argument("--device-index", type=int, default=None,
                        help="Index of the audio device to use. Only used for live input.")
    


    args = parser.parse_args()

    if args.list_devices:
        LiveMicrophoneInput.list_devices()
        sys.exit(0)

    sys.exit(main(args))
