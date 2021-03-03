Feature: Check if correct http error is returned
  Check if correct http error is returned when posting and event with wrong data.

  Scenario Outline: Post events with wrong data
    When post event with data <event_data>
    Then the response code should be <code>

    Examples:
    | event_data | code |
    | {"container": "wrongdata", "storage_account": "devstoreaccount1", "blob_event_type": "Microsoft.Storage.BlobCreated", "blob_type": "BlockBlob"} | 422  |
    | {"container": "oseberg", "storage_account": "wrongdata", "blob_event_type": "Microsoft.Storage.BlobCreated", "blob_type": "BlockBlob"} | 422  |
    | {"container": "oseberg", "storage_account": "devstoreaccount1", "blob_event_type": "wrongdata", "blob_type": "BlockBlob"} | 422  |
    | {"container": "oseberg", "storage_account": "devstoreaccount1", "blob_event_type": "Microsoft.Storage.BlobCreated", "blob_type": "wrongdata"} | 422  |