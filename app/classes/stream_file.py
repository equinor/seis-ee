from datetime import datetime

from decimate import decimate_grane, decimate_oseberg, decimate_snorre
from settings import FieldStorageContainers
from transfer import transfer_file


class StreamFile:
    def __init__(self, path: str, format: FieldStorageContainers):
        self.path = path
        self.format: FieldStorageContainers = format
        self.decimated_path: str = ""

    # TODO: After decimation, upload result file to Azure Files and delete from disk.
    # TODO: This could perhaps be done async. ONLY IF we need the performance
    def decimate(self):
        # TODO  Check headers , event, now(), or something
        date = datetime.now()
        date_path = f"{date.year}/{date.month}/{date.day}"

        if self.format == FieldStorageContainers.OSEBERG:
            output_dir = f"data/oseberg/{date_path}"
            self.decimated_path = decimate_oseberg(self.path, destination=output_dir)

        elif self.format == FieldStorageContainers.GRANE:
            output_dir = f"data/grane/{date_path}"
            self.decimated_path = decimate_grane(self.path, destination=output_dir)

        elif self.format == FieldStorageContainers.SNORRE:
            output_dir = f"data/snorre/{date_path}"
            self.decimated_path = decimate_snorre(self.path, destination=output_dir)

    def transfer(self):
        transfer_file(self.path)

    def __repr__(self):
        return f"Path: {self.path}, Format: {self.format.value}, Decimated: {self.decimated_path}"
