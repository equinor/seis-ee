import json

from behave import then, when
from fastapi.testclient import TestClient

from event_listener import app

client = TestClient(app)


@when("a request is POST(ED) at the {url} location")
def post_request(context, url: str):
    as_json = json.loads(context.text)
    response = client.post(url, json=as_json)
    context.response = response


@then("the response code should be {code}")
def check_status(context, code: int):
    assert context.response.status_code == int(code)


@when("post event with data {event_data}")
def send_request_with_data(context, event_data: str):
    event_data_obj = json.loads(event_data)
    event = [
        {
            "topic": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myrg/providers/"
            "Microsoft.Storage/storageAccounts/myblobstorageaccount",
            "subject": "/blobServices/default/containers/testcontainer/blobs/testfile.txt",
            "eventType": f"{event_data_obj['blob_event_type']}",
            "eventTime": "2017-08-16T20:33:51.0595757Z",
            "id": "4d96b1d4-0001-00b3-58ce-16568c064fab",
            "data": {
                "api": "PutBlockList",
                "clientRequestId": "d65ca2e2-a168-4155-b7a4-2c925c18902f",
                "requestId": "4d96b1d4-0001-00b3-58ce-16568c000000",
                "eTag": "0x8D4E4E61AE038AD",
                "contentType": "text/plain",
                "contentLength": "123",
                "blobType": f"{event_data_obj['blob_type']}",
                "url": f"https://{event_data_obj['storage_account']}.blob.core.windows.net/"
                f"{event_data_obj['container']}/test_data/oseberg/oseberg-test.su",
                "sequencer": "00000000000000EB0000000000046199",
                "storageDiagnostics": {"batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"},
            },
            "dataVersion": "",
            "metadataVersion": "1",
        }
    ]
    event_string = json.dumps(event)
    response = client.post("/events?secret=dummy", json=event_string)
    context.response = response
