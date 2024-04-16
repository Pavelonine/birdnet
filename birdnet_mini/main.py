import sys
from pathlib import Path

from birdnet_mini.audio import open_audio_file, split_signal
from birdnet_mini.model import Model

SCRIPT_DIR = Path(__file__).resolve().parent
TEST_FILE_PATH = SCRIPT_DIR / ".." / "testdata" / "test_1min.wav"
MODEL_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Model_FP32.tflite"
LABELS_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Labels.txt"


def main():
    # load the sample chunks from file
    sig, rate = open_audio_file(str(TEST_FILE_PATH))
    chunks = split_signal(sig, rate, 3.0, 0.0, 1.0)

    # load the labels
    with open(LABELS_FILE_PATH, "r") as f:
        labels = f.read().splitlines()

    # load the model
    model = Model(str(MODEL_FILE_PATH), labels)

    # predict the chunks
    prediction = model.predict(chunks[0])

    # print the predictions
    for label_idx, label, score in prediction[:5]:
        print(f"{label_idx:04d} {label}: {score}")


if __name__ == "__main__":
    sys.exit(main())
