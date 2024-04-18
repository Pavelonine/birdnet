import glob
from pathlib import Path

from birdnet_mini.metadata import MetaData

AUDIO_FOLDER_PATH = Path("k:") / "science-camp" / "Data"
METADATA_FILE_PATH = Path("k:") / "science-camp" / "SMM11597_Summary.txt"

metad = MetaData(METADATA_FILE_PATH)
files = glob.glob(str(AUDIO_FOLDER_PATH / "*.wav"))

for file in files:
    file_ts, file_lat, file_lon = metad.get_timestamp_lat_lon(str(Path(file).stem))
    if file_ts is None:
        print(f"No metadata found for {file}")