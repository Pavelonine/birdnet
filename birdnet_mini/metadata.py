from datetime import datetime


class MetaData:
    def __init__(self, metadata_file):
        self.metadata = self._read_metadata(metadata_file)

    @staticmethod
    def _read_metadata(metadata_file):
        """
        Read the metadata file of the Wildlife Acoustic recorders. and return a dictionary with the metadata.
        The dictionary has the following structure: key: timestamp, value: (lat, lon)

        :param metadata_file: path to the metadata file
        :return:
        """
        with open(metadata_file, "r") as f:
            metadata_lines = f.read().splitlines()
        metadata = dict()
        for m_entry in metadata_lines:
            parts = m_entry.split(",")
            if parts[0] == "DATE":
                continue  # headline
            timestamp_string = parts[0] + " " + parts[1]
            lat = float(parts[2]) if parts[3] == "N" else -float(parts[2])
            lon = float(parts[4]) if parts[5] == "E" else -float(parts[4])
            timestamp = datetime.strptime(timestamp_string, "%Y-%b-%d %H:%M:%S")
            metadata[timestamp] = (lat, lon)
        return metadata

    def get_timestamp_lat_lon(self, filename_stem: str):
        try:
            timestamp = self.parse_timestamp_from_filename(filename_stem)
            return (timestamp, ) + self.metadata[timestamp]
        except KeyError:
            return None, None, None

    @staticmethod
    def parse_timestamp_from_filename(filename_stem: str):
        try:
            parts = filename_stem.split("_")
            datetime_str = parts[1] + " " + parts[2]
            return datetime.strptime(datetime_str, "%Y%m%d %H%M%S")
        except (IndexError, ValueError):
            print(f"[metdata] Error parsing timestamp from filename {filename_stem}")
            return None
