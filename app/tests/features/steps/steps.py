import json
from datetime import datetime
from pathlib import Path
from utils import is_valid_file_format
from behave import given, when, then

from classes.event import Event
from event_listener import events
from services.az_files_service import az_files_service
from services.blob_service import BlobService
from services.queue_service import convert_queue
from settings import FieldStorageContainers
from azure.storage.queue import QueueMessage
from mseed_converter import convert_to_mseed


@given("there are OSEBERG files in the blob storage")
def test_data_oseberg(context):
    BlobService(FieldStorageContainers.OSEBERG).upload_blob(str(Path("test_data/oseberg/oseberg-test.su").absolute()))


@given("there are GRANE files in the blob storage")
def test_data_grane(context):
    BlobService(FieldStorageContainers.GRANE).upload_blob(str(Path("test_data/grane/grane-test.sgd").absolute()))


@given("there are SNORRE files in the blob storage")
def test_data_snorre(context):
    BlobService(FieldStorageContainers.SNORRE).upload_blob(str(Path("test_data/snorre/snorre-test.sgd").absolute()))


@when("an event is posted")
def step_impl2(context):
    event = Event.parse_raw(context.text)
    context.event = event
    context.response = events([event], "dummy")


@then('the decimated file "{filename}" gets uploaded')
def step_impl3(context, filename):
    event: Event = context.event
    date = datetime.now()
    date_path = f"{date.year}/{date.month}/{date.day}"
    assert az_files_service.file_exists(f"{event.data.field.value}/{date_path}/{filename}")


@then("the response will be")
def step_impl4(context):
    expected = json.loads(context.text)
    actual = context.response
    assert expected == actual


@given("an empty convert-queue")
def step_impl6(context):
    convert_queue.clear_messages()


@when("a message is sent")
def step_impl7(context):
    convert_queue.send_message({"Some": "Data", "Foo": "Bar"})


@then("the queues contains messages")
def step_impl8(context):
    convert_msg = convert_queue.fetch_message()
    assert convert_msg


@then("add message to convert-queue with format {format} and path {path}")
def add_msg_to_convert_queue(context, format, path):
    convert_queue.send_message({"format": format.replace('"', ""), "path": path.replace('"', "")})


@then("the file {file} has been created in {target_dir}")
def step_impl(context, file, target_dir):
    convert_msg: QueueMessage = convert_queue.fetch_message()
    message_content: dict = json.loads(convert_msg.content)
    azure_storage_decimated_file_path: str = message_content["path"]
    file_format: str = message_content["format"]
    if is_valid_file_format(file_format):
        convert_to_mseed(azure_storage_decimated_file_path)
    convert_to_mseed(azure_storage_decimated_file_path)

    # todo add an assert to check if file has been created - when mseed converter is finished
