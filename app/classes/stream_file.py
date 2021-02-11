from datetime import datetime
from pathlib import Path

from decimate import decimate_oseberg, decimate_grane

from settings import FileFormat
from transfer import transfer_file


class StreamFile:
    def __init__(self, path: str, format: FileFormat):
        self.path = path
        self.format: FileFormat = format
        self.decimated_path: str = ""

    # TODO: After decimation, upload result file to Azure Files and delete from disk.
    # TODO: This could perhaps be done async. ONLY IF we need the performance
    def decimate(self):
        # Check headers , event, now(), or something
        date = datetime.now()
        date_path = f"{date.year}/{date.month}/{date.day}"
        if self.format == FileFormat.SU_OSEBERG:
            output_dir = f"data/oseberg/{date_path}"
            decimate_oseberg(self.path, destination=output_dir)
            self.decimated_path = output_dir + "/" + Path(self.path).stem + ".ccs.segy"
        elif self.format == FileFormat.SEGD_GRANE:
            output_dir = f"data/decimated_grane_files/{date_path}"
            decimate_grane(self.path, destination=output_dir)
            # TODO: Is this right suffix?
            self.decimated_path = output_dir + "/" + Path(self.path).stem + ".ccs.segy"
        elif self.format == FileFormat.SEGD_SNORRE:
            raise NotImplementedError("Decimation for Snorre files is not supported yet")

    def transfer(self):
        transfer_file(self.path)

    # @classmethod
    # def from_dict(cls, a_dict):
    #     return cls(**a_dict)
    #
    # @classmethod
    # def from_tuple(cls, a_tuple):
    #     return cls(path=a_tuple[0], decimated=a_tuple[1],
    #                transferred=a_tuple[2], decimated_path=a_tuple[3], format=FileFormat[a_tuple[4]])
    #
    # def to_dict(self):
    #     return {
    #         "path": self.path,
    #         "decimated": self.decimated,
    #         "transferred": self.transferred,
    #         "decimated_path": self.decimated_path
    #     }
    #
    # def to_tuple(self):
    #     return self.path, self.decimated, self.transferred, self.decimated_path, self.format.value

    def __repr__(self):
        return f"Path: {self.path}, Decimated: {self.decimated}, Transferred: {self.transferred}"
