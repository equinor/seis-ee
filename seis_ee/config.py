import os


class Config:
    decimated_files_dest = os.getenv("DECIMATED_FILES_DEST", "decimated_files")