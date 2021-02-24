import json

from azure.core.exceptions import ResourceExistsError
from azure.storage.queue import QueueClient, QueueMessage

from settings import settings


class AzQueueService:
    def __init__(self, name: str):
        self.conn_str = settings.QUEUE_CONN_STRING
        self.name = f"{settings.ENVIRONMENT}-{name}"
        self.client = QueueClient.from_connection_string(self.conn_str, self.name)
        try:
            self.client.create_queue()
        except ResourceExistsError:
            pass

    def send_message(self, message: dict):
        self.client.send_message(json.dumps(message), time_to_live=259200)  # ttl: seconds

    def fetch_message(self):
        messages = self.client.receive_messages()
        for msg in messages:
            return msg

    def delete_message(self, message: QueueMessage):
        self.client.delete_message(message)

    def clear_messages(self):
        self.client.clear_messages()


stream_queue = AzQueueService("stream")
convert_queue = AzQueueService("convert")
