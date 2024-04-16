import sys
import argparse
from pathlib import Path

import numpy as np
from scipy import signal

import matplotlib.pyplot as plt

from birdnet_mini.audio import get_raw_audio_chunks_from_file, save_signal, open_audio_file, split_signal
from birdnet_mini.model import Model

SCRIPT_DIR = Path(__file__).resolve().parent
TEST_FILE_PATH = SCRIPT_DIR / ".." / "testdata" / "test_1min.wav"
MODEL_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Model_FP32.tflite"
LABELS_FILE_PATH = SCRIPT_DIR / "models" / "BirdNET_GLOBAL_6K_V2.4_Labels.txt"


def main():
    # load the sample chunks from file
    sig, rate = open_audio_file(str(TEST_FILE_PATH))
    chunks = split_signal(sig, rate, 3.0, 0.0, 1.0)

    # # plot the samples for the first chunk
    # plt.plot(chunks[0])
    # plt.xlabel("Sample")
    # plt.ylabel("Amplitude")
    #
    # plt.figure()
    # # plot the spectrogram for the first chunk
    # frequencies, times, spectrogram = signal.spectrogram(chunks[0], 48000)
    # plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='auto')
    # plt.ylabel('Frequency (Hz)')
    # plt.xlabel('Time (s)')
    # plt.colorbar(label='Power Spectral Density (dB)')
    # plt.title('Spectrogram')
    #
    # plt.show()


    # load the labels
    with open(LABELS_FILE_PATH, "r") as f:
        labels = f.read().splitlines()

    # load the model
    model = Model(str(MODEL_FILE_PATH), labels)

    # predict the chunks
    predictions = []
    prediction = model.predict(chunks[0])
    predictions.append(prediction)
    for label_idx, label, score in prediction[:5]:
        print(f"{label_idx:04d} {label}: {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BirdNet Mini")
    sys.exit(main())
