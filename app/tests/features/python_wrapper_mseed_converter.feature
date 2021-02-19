
Feature: Convert decimated files to mseed format
  Convert decimated files to mseed format using an external converter program

  Scenario: There are messages in the "convert queue"
    Given an empty convert-queue
    Then add message to convert-queue with format "grane" and path "grane/2021/2/18/grane-test.ccs-grane.dsgd"
    # todo also check oseberg and snorre files....
    Then the file "grane-test.ccs-grane.mseed" has been created in "targetdir"
