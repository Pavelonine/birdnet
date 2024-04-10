import sys
import argparse
from pathlib import Path

import numpy as np
from scipy import signal

import matplotlib.pyplot as plt

from birdnet_mini.audio import get_raw_audio_chunks_from_file, save_signal

SCRIPT_DIR = Path(__file__).resolve().parent
TEST_FILE_PATH = SCRIPT_DIR / ".." / "testdata" / "test.wav"


def main():
    # load the sample chunks from file
    chunks = get_raw_audio_chunks_from_file(str(TEST_FILE_PATH))

    # plot the samples for the first chunk
    plt.plot(chunks[0])
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    plt.figure()
    # plot the spectrogram for the first chunk
    frequencies, times, spectrogram = signal.spectrogram(chunks[0], 48000)
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='auto')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.colorbar(label='Power Spectral Density (dB)')
    plt.title('Spectrogram')

    plt.show()

    # save the first chunk to a file for listening inspection
    save_signal(chunks[0], "chunk.wav")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BirdNet Mini")
    sys.exit(main())
