Feature: Authenticate the event request

  Scenario: An event with a valid secret is posted
    When a request is POST(ED) at the /events?secret=dummy location
    """
    [{
      "topic": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myrg/providers/Microsoft.Storage/storageAccounts/myblobstorageaccount",
      "subject": "/blobServices/default/containers/testcontainer/blobs/testfile.txt",
      "eventType": "Microsoft.Storage.BlobCreated",
      "eventTime": "2017-08-16T20:33:51.0595757Z",
      "id": "4d96b1d4-0001-00b3-58ce-16568c064fab",
      "data": {
        "api": "PutBlockList",
        "clientRequestId": "d65ca2e2-a168-4155-b7a4-2c925c18902f",
        "requestId": "4d96b1d4-0001-00b3-58ce-16568c000000",
        "eTag": "0x8D4E4E61AE038AD",
        "contentType": "text/plain",
        "contentLength": "123",
        "blobType": "THIS_IS_WRONG_AND_WILL_CAUSE_EARLY_FAILURE",
        "url": "https://devstoreaccount1.blob.core.windows.net/oseberg/test_data/oseberg/oseberg-test.su",
        "sequencer": "00000000000000EB0000000000046199",
        "storageDiagnostics": {
          "batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"
        }
      },
      "dataVersion": "",
      "metadataVersion": "1"
    }]
    """
    Then the response code should be 400

  Scenario: An event with an invalid secret is posted
    When a request is POST(ED) at the /events?secret=bad location
    """
    [{
      "topic": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myrg/providers/Microsoft.Storage/storageAccounts/myblobstorageaccount",
      "subject": "/blobServices/default/containers/testcontainer/blobs/testfile.txt",
      "eventType": "Microsoft.Storage.BlobCreated",
      "eventTime": "2017-08-16T20:33:51.0595757Z",
      "id": "4d96b1d4-0001-00b3-58ce-16568c064fab",
      "data": {
        "api": "PutBlockList",
        "clientRequestId": "d65ca2e2-a168-4155-b7a4-2c925c18902f",
        "requestId": "4d96b1d4-0001-00b3-58ce-16568c000000",
        "eTag": "0x8D4E4E61AE038AD",
        "contentType": "text/plain",
        "contentLength": "123",
        "blobType": "THIS_IS_WRONG_AND_WILL_CAUSE_EARLY_FAILURE",
        "url": "https://devstoreaccount1.blob.core.windows.net/oseberg/test_data/oseberg/oseberg-test.su",
        "sequencer": "00000000000000EB0000000000046199",
        "storageDiagnostics": {
          "batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"
        }
      },
      "dataVersion": "",
      "metadataVersion": "1"
    }]
    """
    Then the response code should be 401
