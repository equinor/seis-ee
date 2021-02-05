import subprocess
from pathlib import Path

from settings import settings
from utils import logger


def ensure_remote_path(path: str):
    try:
        subprocess.run(args=f"ssh {settings.STREAM_TARGET_USER}@{settings.STREAM_TARGET_HOST} mkdir -p {path}",
                       shell=True, check=True, capture_output=True, encoding="UTF-8")
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        raise e


def transfer_file(target: str):
    _dest = target.split("/")[-3:]
    dest = f"{settings.STREAM_TARGET_DIR}/{'/'.join(_dest)}"
    ensure_remote_path(str(Path(dest).parent))
    logger.info(f"Transfering '{target}' to '{settings.STREAM_TARGET_USER}@{settings.STREAM_TARGET_HOST}:{dest}'")
    try:
        subprocess.run(
            args=f"rsync -vA {target} {settings.STREAM_TARGET_USER}@{settings.STREAM_TARGET_HOST}:{dest}",
            shell=True, check=True, capture_output=True, encoding="UTF-8")
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        raise e
