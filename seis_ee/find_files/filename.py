from datetime import datetime, timedelta
from pathlib import Path

from utils import logger


def grane_path_to_dates(path: Path):
    # Try splitting the filename
    elements = path.name.split("-")
    if len(elements) < 5:
        logger.debug(f"Skipping file; {str(path)}")
        return

    try:
        first_date = datetime(year=int(elements[0]), month=int(elements[1]), day=int(elements[2]),
                              hour=int(elements[3]), minute=int(elements[4]), second=int(elements[5]))
    except Exception as e:
        logger.info(f"Failed to parse filename into date; {path.name}")
        logger.info(e)
        return
    return {"path": path, "from": first_date, "to": first_date + timedelta(seconds=8)}
