import sys
import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from birdnet_mini.audio import get_raw_audio_chunks_from_file, save_signal

SCRIPT_DIR = Path(__file__).resolve().parent
TEST_FILE_PATH = SCRIPT_DIR / ".." / "testdata" / "test.wav"


def main():
    # load the sample chunks from file
    chunks = get_raw_audio_chunks_from_file(str(TEST_FILE_PATH))

    # plot the samples for the first chunk
    plt.plot(chunks[0])
    plt.show()

    # save the first chunk to a file for listening inspection
    save_signal(chunks[0], "chunk.wav")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BirdNet Mini")
    sys.exit(main())
