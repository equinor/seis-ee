from datetime import datetime
from pathlib import Path

from behave import *

from classes.event import Event
from event_listener import events, format_from_blob_url
from services.az_files_service import az_files_service
from services.blob_service import blob_service


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
