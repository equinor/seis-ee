Feature: Validate an Azure Event Subscription
  Azure Event Subscriptions needs to be validated via a two-way-handshake
  https://docs.microsoft.com/en-us/azure/event-grid/webhook-event-delivery

  Scenario: An Event Subscription sends a validation request to specified endpoint
    When an event is posted
    """
    {
      "id": "2d1781af-3a4c-4d7c-bd0c-e34b19da4e66",
      "topic": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "subject": "",
      "data": {
        "validationCode": "512d38b6-c7b8-40c8-89fe-f46f9e9622b6",
        "validationUrl": "https://rp-eastus2.eventgrid.azure.net:553/eventsubscriptions/estest/validate?id=512d38b6-c7b8-40c8-89fe-f46f9e9622b6&t=2018-04-26T20:30:54.4538837Z&apiVersion=2018-05-01-preview&token=1A1A1A1A"
      },
      "eventType": "Microsoft.EventGrid.SubscriptionValidationEvent",
      "eventTime": "2018-01-25T22:12:19.4556811Z",
      "metadataVersion": "1",
      "dataVersion": "1"
    }
    """
    Then the response will be
    """
    {"validationResponse": "512d38b6-c7b8-40c8-89fe-f46f9e9622b6"}
    """
