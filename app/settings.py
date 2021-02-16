from enum import Enum
from typing import List

from pydantic import BaseSettings


class FieldStorageContainers(Enum):
    OSEBERG = "oseberg"
    GRANE = "grane"
    SNORRE = "snorre"


# Pydantic config loading ref: https://fastapi.tiangolo.com/advanced/settings/
# Will use env variables, and set default. Also parses complex data as json-strings
class Settings(BaseSettings):
    # Azurite default connection string
    QUEUE_CONN_STRING: str = (
        "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "QueueEndpoint=http://localhost:10001/devstoreaccount1;"
    )
    BLOB_CONN_STRING: str = (
        "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://localhost:10000/devstoreaccount1;"
    )
    FILES_CONN_STRING: str
    STORAGE_ACCOUNT: str = "devstoreaccount1"
    FILES_SHARE: str = "ccs-passive"
    DECIMATED_FILES_DEST: str = "decimated_files"
    STREAM_TARGET_USER: str = "kkje"
    STREAM_TARGET_HOST: str = "hnet.norwayeast.cloudapp.azure.com"
    STREAM_TARGET_DIR: str = "/data/kjtest"
    TMP_BLOB_DIR: str = "data/downloads"
    GRANE_SENSORS: List[int] = [10357, 70375]
    OSEBERG_SENSORS: List[int] = [12, 21]
    SNORRE_SENSORS: List[int] = [370402, 420424]
    GRANE_SAMPLE_RATE: int = 4500
    SNORRE_SAMPLE_RATE: int = 1250
    SNORRE_FILE_HEADER_SIZE: int = 192
    GRANE_FILE_HEADER_SIZE: int = 160
    ENVIRONMENT: str = "dev"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
