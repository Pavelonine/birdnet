"""Module containing audio helper functions.
"""
import soundfile as sf
import librosa
import numpy as np


RANDOM_SEED = 42
RANDOM = np.random.RandomState(RANDOM_SEED)


INFERENCE_SAMPLE_RATE = 48000
# We're using 3-second chunks
SIG_LENGTH: float = 3.0

# Define overlap between consecutive chunks <3.0; 0 = no overlap
SIG_OVERLAP: float = 0

# Define minimum length of audio chunk for prediction,
# chunks shorter than 3 seconds will be padded with zeros
SIG_MINLEN: float = 1.0

# Frequency range. This is model specific and should not be changed.
SIG_FMIN = 0
SIG_FMAX = 15000

BANDPASS_FMIN: int = 0
BANDPASS_FMAX: int = 15000


def get_raw_audio_chunks_from_file(fpath: str, offset=0, duration=None):
    """Reads an audio file.

    Reads the file and splits the signal into chunks.

    Args:
        fpath: Path to the audio file.

    Returns:
        The signal split into a list of chunks.
    """
    # Open file
    sig, rate = open_audio_file(fpath, INFERENCE_SAMPLE_RATE, offset, duration)

    # Split into raw audio chunks
    chunks = split_signal(sig, rate, SIG_LENGTH, SIG_OVERLAP, SIG_MINLEN)

    return chunks


def open_audio_file(path: str, sample_rate=48000, offset=0.0, duration=None):
    """Open an audio file.

    Opens an audio file with librosa and the given settings.

    Args:
        path: Path to the audio file.
        sample_rate: The sample rate at which the file should be processed.
        offset: The starting offset in seconds.
        duration: Maximum duration of the loaded content.

    Returns:
        Returns the audio time series and the sampling rate.
    """
    sig, rate = librosa.load(path, sr=sample_rate, offset=offset, duration=duration, mono=True, res_type="kaiser_fast")
    return sig, rate


def save_signal(sig, fname: str):
    """Saves a signal to file.

    Args:
        sig: The signal to be saved.
        fname: The file path.
    """
    sf.write(fname, sig, 48000, "PCM_16")


def noise(sig, shape, amount=None):
    """Creates noise.

    Creates a noise vector with the given shape.

    Args:
        sig: The original audio signal.
        shape: Shape of the noise.
        amount: The noise intensity.

    Returns:
        An numpy array of noise with the given shape.
    """
    # Random noise intensity
    if amount is None:
        amount = RANDOM.uniform(0.1, 0.5)

    # Create Gaussian noise
    try:
        result_noise = RANDOM.normal(min(sig) * amount, max(sig) * amount, shape)
    except:
        result_noise = np.zeros(shape)

    return result_noise.astype("float32")


def split_signal(sig, rate, seconds, overlap, min_len):
    """Split signal with overlap.

    Args:
        sig: The original signal to be split.
        rate: The sampling rate.
        seconds: The duration of a segment.
        overlap: The overlapping seconds of segments.
        min_len: Minimum length of a split.
    
    Returns:
        A list of splits.
    """
    sig_splits = []

    for i in range(0, len(sig), int((seconds - overlap) * rate)):
        split = sig[i: i + int(seconds * rate)]

        # End of signal?
        if len(split) < int(min_len * rate) and len(sig_splits) > 0:
            break

        # Signal chunk too short?
        if len(split) < int(rate * seconds):
            split = np.hstack((split, noise(split, (int(rate * seconds) - len(split)), 0.5)))

        sig_splits.append(split)

    return sig_splits
