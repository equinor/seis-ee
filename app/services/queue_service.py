import json

from azure.core.exceptions import ResourceExistsError
from azure.storage.queue import QueueClient, QueueMessage

from settings import settings


class AzQueueService:
    def __init__(self, name: str):
        self.conn_str = settings.STORAGE_CONN_STRING
        self.name = f"{settings.ENVIRONMENT}-{name}"
        self.client = QueueClient.from_connection_string(self.conn_str, self.name)
        try:
            self.client.create_queue()
        except ResourceExistsError:
            pass

    def send_message(self, message: dict):
        self.client.send_message(json.dumps(message), time_to_live=3)  # ttl: days

    def fetch_message(self):
        messages = self.client.receive_messages()
        for msg in messages:
            return msg

    def delete_message(self, message: QueueMessage):
        self.client.delete_message(message)


stream_queue = AzQueueService("stream")
convert_queue = AzQueueService("convert")

if __name__ == '__main__':
    stream_queue.send_message({"t": 123})
    message = stream_queue.fetch_message()
    stream_queue.delete_message(message)
