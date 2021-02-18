from utils import logger
import subprocess  # nosec
from settings import FieldStorageContainers
from services.az_files_service import az_files_service

def convert_to_mseed(azure_storage_decimated_file_path: str, file_format: str):
    output_file_path: str = "/data/mseed/" + azure_storage_decimated_file_path

    #download from azure file storage to local storage
    local_file_path: str = az_files_service.download_file(azure_storage_decimated_file_path)

    if (file_format in [item.value for item in FieldStorageContainers]):
        cli_parameters: str = f"{local_file_path} {output_file_path}"
    else:
        raise Exception("Wrong file format")

    try:
        logger.info(f"converting file {local_file_path} to mseed ...")
        # TODO: Secure against Command Injection
        # TODO: substitute the c++ program with the real mseed converter
        mseed_converter_process = subprocess.run(  # noqa
            args=f"cd ..; ./mseed-app/main {cli_parameters}",
            # noqa
            shell=True,  # noqa
            check=True,
            capture_output=True,
            encoding="UTF-8",
        )
        logger.info(mseed_converter_process)
    except subprocess.CalledProcessError as e:
        logger.warning(e.stderr)
        raise Exception(e.stderr)

