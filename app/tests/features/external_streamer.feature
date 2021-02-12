Feature: Stream file 514993.ccs.segy from stream_queue
  if a new message appears in stream_queue, stream this file from azure file storage to a test server

  Scenario: new message is uploaded to blob storage, added to stream_queue and sent to external server
    Given new file is uploaded to blob storage
    And an empty stream-queue
    When an event is posted
    """
    {
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
        "blobType": "BlockBlob",
        "url": "https://devstoreaccount1.blob.core.windows.net/oseberg/test_data/oseberg/514993.su",
        "sequencer": "00000000000000EB0000000000046199",
        "storageDiagnostics": {
          "batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"
        }
      },
      "dataVersion": "",
      "metadataVersion": "1"
    }
    """
    Then the decimated file 514993.cc.segy gets uploaded
    And stream decimated file from azure file storage to server
    And check if file exists on server