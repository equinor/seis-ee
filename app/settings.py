from enum import Enum
from typing import List

from pydantic import BaseSettings


class FieldStorageContainers(Enum):
    OSEBERG = "OSEBERG"
    GRANE = "GRANE"
    SNORRE = "SNORRE"


class FileFormat(Enum):
    SEGD_GRANE = "segd-grane"
    SU_OSEBERG = "su-oseberg"
    SEGD_SNORRE = "segd-snorre"


# Pydantic config loading ref: https://fastapi.tiangolo.com/advanced/settings/
# Will use env variables, and set default. Also parses complex data as json-strings
class Settings(BaseSettings):
    # Azurite default connection string
    QUEUE_CONN_STRING: str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;QueueEndpoint=http://localhost:10001/devstoreaccount1;"
    BLOB_CONN_STRING: str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;"
    FILES_CONN_STRING: str
    STORAGE_ACCOUNT: str = "devstoreaccount1"
    BLOB_STORAGE_CONTAINER: str = "oseberg"
    FILES_SHARE: str = "oseberg"
    DECIMATED_FILES_DEST: str = "decimated_files"
    STREAM_TARGET_USER: str = "kkje"
    STREAM_TARGET_HOST: str = "hnet.norwayeast.cloudapp.azure.com"
    STREAM_TARGET_DIR: str = "/data/kjtest"
    TMP_BLOB_DIR: str = "data/downloads"
    GRANE_SENSORS: List[int] = [1, 2, 3, 5]
    OSEBERG_SENSORS: List[int] = [12, 21]
    SNORRE_SENSORS: List[int] = [1, 2, 3, 5]
    REDUCE_FILES_OPTIONS: List[str] = [FileFormat.SEGD_GRANE.value, FileFormat.SU_OSEBERG.value,
                                       FileFormat.SEGD_SNORRE.value]
    ENVIRONMENT: str = "dev"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
