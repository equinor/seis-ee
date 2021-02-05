from datetime import datetime
from pathlib import Path
from typing import List, Set
from services.database import Database
from classes.stream_file import StreamFile
from settings import FileFormat

# TODO: Agree on a directory structure
from utils import logger


def files_in_todays_directory(target_dir: str, format: str) -> Set[str]:
    date = datetime.now()
    if format == FileFormat.SU_OSEBERG.value:
        path = Path("oseberg/")
    elif format == FileFormat.SEGD_GRANE.value:
        path = Path("grane/")  # todo - update this path when going in production
    elif format == FileFormat.SEGD_SNORRE.value:
        path = Path("snorre/")
    target = Path(path)
    files = [str(x.resolve()) for x in target.rglob("*") if x.is_file()]
    return set(files)


def work_file(file: StreamFile, sensors: List[int]) -> StreamFile:
    if not file.decimated:
        file.decimate(nodes=sensors)
    if not file.transferred:
        file.transfer()
    return file


def continue_unfinished(sensors: List[int], format):
    database = Database(format)
    unfinished = database.all_unfinished()
    for file in unfinished:
        work_file(file, sensors)


def transfer_new_files(new_files: Set[str], database: Database, sensors: [int], processed: Set[str], file_format: str):
    # the parameter set new_files contains path for the new files to stream
    for path in new_files:
        file = StreamFile(path, database, file_format)
        file.insert()
        work_file(file, sensors)
    processed.update(new_files)
    logger.info(f"Transferred {len(new_files)}")
    return processed
