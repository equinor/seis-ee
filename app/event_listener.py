from typing import List

import uvicorn
from azure.core.exceptions import ResourceNotFoundError
from fastapi import FastAPI, HTTPException, status

from classes.event import Event
from classes.stream_file import StreamFile
from exceptions import BadInputException
from services.az_files_service import az_files_service
from services.blob_service import BlobService
from services.queue_service import convert_queue, stream_queue
from settings import FieldStorageContainers, settings
from utils import delete_file, logger

app = FastAPI()


def handle_new_blob_event(event: Event):
    format = event.data.field

    # Download the raw file from the common BlobStorage
    filepath = BlobService(event.data.field).download_blob(event.data.filepath)
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
    if (
        FieldStorageContainers[container.upper()].value != container
        or account != settings.STORAGE_ACCOUNT
        or event.eventType != "Microsoft.Storage.BlobCreated"
        or event.data.blobType != "BlockBlob"
    ):
        return False
    return True


@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
def events(event_list: List[Event]):
    results = []
    for event in event_list:

        # TODO: Verify with shared secret

        # Handle Validation requests first
        if event.eventType == "Microsoft.EventGrid.SubscriptionValidationEvent":
            return {"validationResponse": event.data.validationCode}

        if not validate_event(event):
            logger.warning("Invalid event posted. Reason: Wrong storage account or container")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid event posted")

        try:
            results.append(handle_new_blob_event(event))
        except BadInputException as e:
            logger.warning(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid event posted")
        except ResourceNotFoundError as e:
            logger.warning(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.warning("Something went wrong somewhere...\nA more specific exception should be caught")
            logger.exception(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid event posted")
    return results


if __name__ == "__main__":
    uvicorn.run("event_listener:app", host="0.0.0.0", port=5000, reload=True)
