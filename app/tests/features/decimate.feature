Feature: Download, decimate, and upload on event trigger
  Download a raw seismic file on event trigger, decimate it, and upload result to Azure Files.

  Scenario: An OSEBERG SU file has been uploaded and event triggered
    Given there are OSEBERG files in the blob storage
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
        "url": "https://devstoreaccount1.blob.core.windows.net/oseberg/test_data/oseberg/oseberg-test.su",
        "sequencer": "00000000000000EB0000000000046199",
        "storageDiagnostics": {
          "batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"
        }
      },
      "dataVersion": "",
      "metadataVersion": "1"
    }
    """
    Then the decimated file "oseberg-test.ccs-oseberg.segy" gets uploaded

  Scenario: An SNORRE SEGD file has been uploaded and event triggered
    Given there are SNORRE files in the blob storage
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
        "url": "https://devstoreaccount1.blob.core.windows.net/snorre/test_data/snorre/snorre-test.sgd",
        "sequencer": "00000000000000EB0000000000046199",
        "storageDiagnostics": {
          "batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"
        }
      },
      "dataVersion": "",
      "metadataVersion": "1"
    }
    """
    Then the decimated file "snorre-test.ccs-snorre.dsgd" gets uploaded

  Scenario: An GRANE SEGD file has been uploaded and event triggered
    Given there are GRANE files in the blob storage
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
        "url": "https://devstoreaccount1.blob.core.windows.net/grane/test_data/grane/grane-test.sgd",
        "sequencer": "00000000000000EB0000000000046199",
        "storageDiagnostics": {
          "batchId": "dffea416-b46e-4613-ac19-0371c0c5e352"
        }
      },
      "dataVersion": "",
      "metadataVersion": "1"
    }
    """
    Then the decimated file "grane-test.ccs-grane.dsgd" gets uploaded
