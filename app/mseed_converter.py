from utils import logger, sanitize_shell_arguments, is_valid_file_format
import subprocess  # nosec
from services.az_files_service import az_files_service
from services.queue_service import convert_queue
from azure.storage.queue import QueueMessage
from exceptions import MSeedConvertionException, DownloadFileException
from settings import FieldStorageContainers
import time
import json


def convert_to_mseed(azure_storage_decimated_file_path: str, station: FieldStorageContainers):
    output_file_path: str = "data/mseed/"

    # download from azure file storage to local storage
    local_file: str = az_files_service.download_file(azure_storage_decimated_file_path)
    station_code: str = ""
    if station == FieldStorageContainers.GRANE.value:
        station_code = "GR"
    elif station == FieldStorageContainers.SNORRE.value:
        station_code = "SN"
    elif station == FieldStorageContainers.OSEBERG.value:
        station_code = "OS"
    channel_code: str = "X"
    network_code: str = "NS"
    # todo how to select correct channel_code and network_code?

    converter_app: str
    if station == FieldStorageContainers.SNORRE.value or station == FieldStorageContainers.GRANE.value:
        converter_app = "./segdconv"
    elif station == FieldStorageContainers.OSEBERG.value:
        converter_app = "./segyconv"
    else:
        raise MSeedConvertionException(
            f"wrong file type used as input to function convert_to_mseed(). file type used: {station}"
        )

    cli_parameters: str = f"{sanitize_shell_arguments(local_file)} \
                            {sanitize_shell_arguments(output_file_path)} \
                            {station_code} {channel_code} {network_code}"

    logger.info(f"converting file {local_file} to mseed ...")
    # TODO: substitute the c++ program with the real mseed converter
    mseed_converter_process = subprocess.run(  # noqa
        args=f"{converter_app} {cli_parameters}",
        # noqa
        shell=True,  # noqa
        check=True,
        capture_output=True,
        encoding="UTF-8",
    )
    logger.info(mseed_converter_process)


def poll_convert_queue():
    logger.info("started polling convert queue ...")
    SLEEP_TIME = 10
    msg: QueueMessage
    while True:
        msg = convert_queue.fetch_message()
        if msg:
            logger.info(f"new msg arrived in convert queue! {msg}")
            try:
                message_content = json.loads(msg.content)
                azure_storage_decimated_file_path = message_content["path"]
                station: FieldStorageContainers = message_content["format"]
                if is_valid_file_format(station):
                    convert_to_mseed(azure_storage_decimated_file_path, station)
                    # todo upload mseed file to azure storage
                else:
                    raise MSeedConvertionException(f"Format in message was not valid: {station}")
                convert_queue.delete_message(msg)
            except KeyError as e:
                logger.error(
                    """The convert queue message content could not be read correctly.
                    Skip converting this file to mseed and delete this queue message.""",
                    e,
                )
                convert_queue.delete_message(msg)
            except (MSeedConvertionException, DownloadFileException) as e:
                logger.error(
                    f"""Error occurred when converting decimated file to mseed.
                    Error message: {e}"""
                )
                convert_queue.delete_message(msg)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to run the mseed conversion program through subprocess.run. Error message: {e}")
            except Exception as e:
                logger.error(f"Unknown error occurred when converting decimated file to mseed. Error message: {e}")
        else:
            time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    poll_convert_queue()
