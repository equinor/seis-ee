Feature: Add messages to queues

  Scenario: A decimated file has been uploaded
    Given an empty convert-queue
    When a message is sent
    Then the queues contains messages
