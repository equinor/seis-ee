from utils import logger, sanitize_shell_arguments
import subprocess  # nosec
from settings import FieldStorageContainers
from services.az_files_service import az_files_service
from services.queue_service import convert_queue
from azure.storage.queue import QueueMessage
import time
import json


def convert_to_mseed(azure_storage_decimated_file_path: str, file_format: str):
    output_file_path: str = "/data/mseed/" + azure_storage_decimated_file_path

    # download from azure file storage to local storage
    try:
        local_file: str = az_files_service.download_file(azure_storage_decimated_file_path)
    except Exception as e:
        raise Exception(
            f"For mseed conversion, could not download the specified file from azure file storage. Error message: {e}"
        )

    if file_format in [item.value for item in FieldStorageContainers]:
        cli_parameters: str = f"{sanitize_shell_arguments(local_file)} {sanitize_shell_arguments(output_file_path)}"
    else:
        raise Exception("Wrong file format for file in convert queue. Could not convert this file to mseed.")

    try:
        logger.info(f"converting file {local_file} to mseed ...")
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
        raise Exception("Something went wrong during mseed conversion. Error message: ", e.stderr)


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
                file_format = message_content["format"]
                convert_to_mseed(azure_storage_decimated_file_path, file_format)
            except KeyError as e:
                logger.error(
                    "The convert queue message content could not be read correctly. Skip converting this file to mseed and delete this queue message. ",
                    e,
                )
            except Exception as e:
                logger.error(e)
            except:
                logger.error(
                    "Something went wrong when converting decimated file to mseed. Skip converting this file and delete the queue message."
                )
            convert_queue.delete_message(msg)
        else:
            time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    poll_convert_queue()
