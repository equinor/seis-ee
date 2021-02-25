from pathlib import Path

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.fileshare import ShareClient, ShareDirectoryClient, ShareFileClient, ShareServiceClient

from settings import settings
from utils import logger
from os import path


class AzFilesService:
    def __init__(self):
        self.conn_str = settings.FILES_CONN_STRING
        self.share = f"{settings.ENVIRONMENT}-{settings.FILES_SHARE}"
        self.client = ShareServiceClient.from_connection_string(self.conn_str)
        try:
            self.share_client = ShareClient.from_connection_string(self.conn_str, self.share)
            self.share_client.create_share()
        except ResourceExistsError:
            pass

    def create_directory(self, directory: str) -> ShareDirectoryClient:
        dir_client = ShareDirectoryClient.from_connection_string(self.conn_str, self.share, directory)
        try:
            dir_client.create_directory()
        except ResourceExistsError:
            logger.debug(f"Directory '{directory}' already exists")
        return dir_client

    def upload_file(self, path: str):
        name_to_upload_as = path.replace("data/", "")
        self.create_tree(name_to_upload_as)

        try:
            with open(path, "rb") as source_file:
                data = source_file.read()
                file_client = ShareFileClient.from_connection_string(self.conn_str, self.share, name_to_upload_as)
                logger.info(f"Uploading decimated file to Azure Files: {name_to_upload_as}")
                file_client.upload_file(data)

        except ResourceExistsError as ex:
            logger.error("ResourceExistsError:", ex.message)
        except ResourceNotFoundError as ex:
            logger.error("ResourceNotFoundError:", ex.message)

        return name_to_upload_as

    def download_file(self, azure_storage_path_to_file: str):

        local_file_full_path = "data/" + azure_storage_path_to_file
        local_file_directory = local_file_full_path.rsplit("/", 1)[0]

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(self.conn_str, self.share, azure_storage_path_to_file)

        logger.info(f"Downloading file from azure storage to local folder {local_file_full_path}")

        # create local directory if it does not exist
        if not path.exists(local_file_directory):
            Path(local_file_directory).mkdir(parents=True, exist_ok=True)

        # Open a file for writing bytes on the local system
        with open(local_file_full_path, "wb") as data:
            # Download the file from Azure into a stream
            stream = file_client.download_file()
            # Write the stream to the local file
            data.write(stream.readall())

        return local_file_full_path

    def file_exists(self, path: str) -> bool:
        try:
            file_client = ShareFileClient.from_connection_string(self.conn_str, self.share, path)
            # If getting props does not raise an error, we assume the file exists
            file_client.get_file_properties()
            return True
        except ResourceNotFoundError:
            return False

    # TODO: This can be optimized by starting from bottom
    def create_tree(self, path: str):
        p = Path(path)

        previous_part = ""
        for directory in p.parent.parts:
            self.create_directory(f"{previous_part}{directory}")
            previous_part = previous_part + directory + "/"


az_files_service = AzFilesService()
