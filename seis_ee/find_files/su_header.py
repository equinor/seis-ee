from datetime import timedelta
from pathlib import Path

from extractors.seismic_unix import timerange_of_su_file
from utils import logger


def su_path_to_dates(path: Path):
    # Some simple format checks
    if path.suffix != ".su":
        logger.debug(f"{path.absolute()} is PROBABLY not a seismic unix file. Only checked file suffix.")
        return
    file_from, file_to = timerange_of_su_file(str(path.absolute()))

    # TODO: This assumes the su-file spans 8 seconds
    return {"path": path, "from": file_from, "to": file_from + timedelta(seconds=8)}
