import subprocess
from pathlib import Path

from config import Config
from utils import logger


def ensure_remote_path(path: str):
    try:
        subprocess.run(args=f"ssh {Config.stream_server_user}@{Config.stream_server_host} mkdir -p {path}",
                                          shell=True, check=True, capture_output=True, encoding="UTF-8")
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        raise e


def transfer_file(target: str):
    _dest = target.split("/")[-3:]
    dest = f"{Config.stream_server_dir}/{'/'.join(_dest)}"
    ensure_remote_path(str(Path(dest).parent))
    logger.info(f"Transfering '{target}' to '{Config.stream_server_user}@{Config.stream_server_host}:{dest}'")
    try:
        subprocess.run(
            args=f"rsync -vA {target} {Config.stream_server_user}@{Config.stream_server_host}:{dest}",
            shell=True, check=True, capture_output=True, encoding="UTF-8")
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        raise e


if __name__ == '__main__':
    transfer_file("/home/stig/git/seis-ee/data/decimated_files/2021/1/test.ccs.segy")
