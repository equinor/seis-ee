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
