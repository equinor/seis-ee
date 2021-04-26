
Feature: Convert decimated files to mseed format
  Convert decimated files to mseed format using an external converter program


  #todo: run decimate on these file before scenarios run.... this will create the decimated file in the folder seis-ee/data/grane/*year/month/day*/filename

  Scenario: Message is added to convert queue with Grane file info
    Given an empty convert-queue
    And output file "data/mseed/tempfile.sgy.mseed" does not exist
    Then add message to convert-queue with format "grane" and path "grane/2021/4/20/2021-03-02-17-05-23-Grane3579618.ccs-grane.dsgd"
    Then after converting a "segd" file, "tempfile.sgy.mseed" has been created in "data/mseed"


  Scenario: Message is added to convert queue with Snorre file info
    Given an empty convert-queue
    And output file "data/mseed/tempfile.sgy.mseed" does not exist
    Then add message to convert-queue with format "snorre" and path "snorre/2021/4/20/2021-03-03-08-36-30-Snorre2774534.ccs-snorre.dsgd"
    Then after converting a "segd" file, "tempfile.sgy.mseed" has been created in "data/mseed"


  Scenario: Message is added to convert queue with Oseberg file info
    Given an empty convert-queue
    And output file "data/mseed/tempfile.sgy.mseed" does not exist
    Then add message to convert-queue with format "oseberg" and path "oseberg/2021/4/20/77947.ccs-oseberg.segy"
    Then after converting a "segy" file, "tempfile.sgy.mseed" has been created in "data/mseed"