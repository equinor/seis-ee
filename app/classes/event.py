from typing import Optional

from pydantic import BaseModel, validator

from settings import FieldStorageContainers


class EventData(BaseModel):
    """
    My Cool model
    """
    api: str
    contentType: str
    contentLength: int
    blobType: str
    url: str
    field: Optional[str]

    # Pydantic stuff to have a derived value
    # https://pydantic-docs.helpmanual.io/usage/validators/
    @validator("field", always=True)
    def validate_field(cls, value, values):
        return cls.field_from_url(values["url"])

    @staticmethod
    def field_from_url(url):
        container = url.split("/")[3]
        if container.upper() == FieldStorageContainers.OSEBERG.value:
            return FieldStorageContainers.OSEBERG.value
        if container.upper() == FieldStorageContainers.GRANE.value:
            return FieldStorageContainers.GRANE.value
        if container.upper() == FieldStorageContainers.SNORRE.value:
            return FieldStorageContainers.SNORRE.value
        raise ValueError("Failed to extract container/field from event url'")


class Event(BaseModel):
    topic: str
    subject: str
    eventType: str
    eventTime: str
    id: str
    data: EventData
