from enum import Enum
from typing import List
from pydantic import BaseSettings
import os


class FieldStorageContainers(Enum):
    OSEBERG = "oseberg"
    GRANE = "grane"
    SNORRE = "snorre"


# Pydantic config loading ref: https://fastapi.tiangolo.com/advanced/settings/
# Will use env variables, and set default. Also parses complex data as json-strings
class Settings(BaseSettings):
    FILES_CONN_STRING: str
    BLOB_CONN_STRING: str
    QUEUE_CONN_STRING: str
    ENVIRONMENT: str
    EVENT_SECRET: str = "dummy"
    STORAGE_ACCOUNT: str = "devstoreaccount1" if os.getenv("ENVIRONMENT") == "dev" else "ccs"
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

    # This is just for local debugging. Environment variables should be injected via docker-compose/kubernetes
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
