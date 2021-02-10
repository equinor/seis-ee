from datetime import datetime
from pathlib import Path

from behave import *

from classes.event import Event
from event_listener import events
from services.az_files_service import az_files_service
from services.blob_service import blob_service
from services.queue_service import convert_queue, stream_queue


@given("there are files in the blob storage")
def step_impl(context):
    blob_service.upload_blob(str(Path("test_data/oseberg/514992.su").absolute()))


@when("an event is posted")
def step_impl(context):
    event = Event.parse_raw(context.text)
    context.event = event
    events([event])


@then("the decimated file gets uploaded")
def step_impl(context):
    event: Event = context.event
    date = datetime.now()
    date_path = f"{date.year}/{date.month}/{date.day}"
    assert az_files_service.file_exists(f"{event.data.field}/{date_path}/514992.ccs.segy")


@then("added to the queues")
def step_impl(context):
    # TODO: Can't request specific message. Do something smart
    pass


@given("an empty stream-queue")
def step_impl(context):
    stream_queue.clear_messages()


@step("an empty convert-queue")
def step_impl(context):
    convert_queue.clear_messages()


@when("a message is sent")
def step_impl(context):
    stream_queue.send_message({"Hallo": "sTream"})
    convert_queue.send_message({"Some": "Data", "Foo": "Bar"})


@then("the queues contains messages")
def step_impl(context):
    stream_msg = stream_queue.fetch_message()
    convert_msg = convert_queue.fetch_message()
    assert stream_msg
    assert convert_msg
