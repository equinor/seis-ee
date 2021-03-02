import os
from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, BlobServiceClient

from settings import FieldStorageContainers, settings
from utils import logger


class BlobService:
    def __init__(self, container: FieldStorageContainers):
        self.container: FieldStorageContainers = container
        self.client = BlobServiceClient.from_connection_string(settings.BLOB_CONN_STRING)
        try:
            self.client.create_container(self.container.value)
        except ResourceExistsError:
            pass

    def blob_client(self, filename: str) -> BlobClient:
        return self.client.get_blob_client(container=self.container.value, blob=filename)

    def upload_blob(self, path: str):
        logger.debug(f"Uploading to Azure Storage as blob: {path}")
        with open(path, "rb") as data:
            name_to_upload_as = path.replace(os.getcwd() + "/", "")
            self.blob_client(name_to_upload_as).upload_blob(data, overwrite=True)

    def download_blob(self, filename: str) -> str:
        dirs = filename.replace(Path(filename).name, "")
        Path(f"{settings.TMP_BLOB_DIR}/{dirs}").mkdir(parents=True, exist_ok=True)
        with open(f"{settings.TMP_BLOB_DIR}/{filename}", "wb") as blob_file:
            raw = self.blob_client(filename).download_blob().readall()
            if raw == b"":
                raise Exception("Tried to decimate an empty file.")
            blob_file.write(raw)
        return str(Path(f"{settings.TMP_BLOB_DIR}/{filename}").absolute())
