from typing import Optional, Union

from pydantic import BaseModel, PydanticValueError, validator

from exceptions import BadInputException
from settings import FieldStorageContainers
from utils import logger, sanitize_shell_arguments


class EventData(BaseModel):
    api: str
    contentType: str
    contentLength: int
    blobType: str
    url: str
    filepath: Optional[str]
    field: Optional[FieldStorageContainers]

    # Pydantic stuff to have a derived value
    # https://pydantic-docs.helpmanual.io/usage/validators/
    @validator("field", always=True)
    def validate_field(cls, value, values):
        if not values.get("url"):
            raise ValueError
        return cls.field_from_url(values["url"])

    @validator("filepath", always=True)
    def validate_filepath(cls, value, values):
        if not values.get("url"):
            raise ValueError
        filename = values["url"].split("/", 4)[4]
        try:
            return sanitize_shell_arguments(filename)
        except BadInputException as e:
            raise PydanticValueError(msg_template=e.message)

    @staticmethod
    def field_from_url(url):
        container = url.split("/")[3]
        if container == FieldStorageContainers.OSEBERG.value:
            return FieldStorageContainers.OSEBERG
        if container == FieldStorageContainers.GRANE.value:
            return FieldStorageContainers.GRANE
        if container == FieldStorageContainers.SNORRE.value:
            return FieldStorageContainers.SNORRE
        msg = f"Failed to extract container/field from event url. Unrecognized container '{container}'"
        logger.error(msg)
        raise ValueError(msg)


class SubscriptionValidation(BaseModel):
    validationCode: str
    validationUrl: str


class Event(BaseModel):
    topic: str
    subject: str
    eventType: str
    eventTime: str
    id: str
    # Pydantic will pick the first type that matches
    data: Union[EventData, SubscriptionValidation]
