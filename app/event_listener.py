from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status

from classes.event import Event
from services.az_files_service import az_files_service
from services.blob_service import blob_service
from services.queue_service import convert_queue, stream_queue
from settings import FieldStorageContainers, FileFormat, settings
from streamer import StreamFile
from utils import logger

app = FastAPI()


def sensors_by_field(field: FileFormat):
    if field == FileFormat.SU_OSEBERG:
        return settings.OSEBERG_SENSORS
    if field == FileFormat.SEGD_SNORRE:
        return settings.SNORRE_SENSORS
    if field == FileFormat.SEGD_GRANE:
        return settings.GRANE_SENSORS
    raise ValueError(f"Invalid file format '{field}'")


def delete_file(path: str):
    try:
        Path(path).unlink()
    except FileNotFoundError:
        logger.error(f"FileNotFoundError: Failed to delete file: '{path}'")


def format_from_blob_url(url: str):
    container = url.split("/")[3]
    if container.upper() == FieldStorageContainers.OSEBERG.value:
        return FileFormat.SU_OSEBERG
    if container.upper() == FieldStorageContainers.GRANE.value:
        return FileFormat.SEGD_GRANE
    if container.upper() == FieldStorageContainers.SNORRE.value:
        return FileFormat.SEGD_SNORRE
    raise ValueError(f"Failed to extract implied file format from BlobContainer '{container}'")


def handle_new_blob_event(event: Event):
    format = format_from_blob_url(event.data.url)
    filename = event.data.url.split("/", 4)[4]

    # Download the raw file from the common BlobStorage
    filepath = blob_service.download_blob(filename)
    file = StreamFile(filepath, format)

    # Decimate the file
    file.decimate()

    # Upload the decimated file to AzureFiles
    uploaded_path = az_files_service.upload_file(file.decimated_path)

    # Add new messages to the queues
    stream_queue.send_message({"format": format.value, "path": uploaded_path})
    convert_queue.send_message({"format": format.value, "path": uploaded_path})

    # Cleanup
    delete_file(filepath)
    delete_file(file.decimated_path)
    return f"Successfully decimated {event.data.url} and uploaded result to FileStorage"


# TODO: Should add some more validation here. Block on IP or something
def validate_event(event: Event):
    account = event.data.url.split("/")[2].split(".")[0]
    container = event.data.url.split("/")[3]
    if account != settings.STORAGE_ACCOUNT or \
            container != settings.BLOB_STORAGE_CONTAINER or \
            event.eventType != 'Microsoft.Storage.BlobCreated' or \
            event.data.blobType != "BlockBlob":
        return False
    return True


@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
def events(event_list: List[Event]):
    results = []
    for event in event_list:
        if not validate_event(event):
            logger.warning("Invalid event posted. Reason: Wrong storage account or container")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid event posted")
        results.append(handle_new_blob_event(event))
    return results


if __name__ == "__main__":
    uvicorn.run("event_listener:app", host="0.0.0.0", port=5000, reload=True)
