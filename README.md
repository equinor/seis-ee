# Seis-EE
_Seismic data event extractor_

## What is Seis-EE
Seis-EE simplifies the process of extracting seismic data from a ranges of dates and times, and a subset of sensor nodes. Useful for looking closer at some seismic events, where time and place is some what limited and known.

## Quick Start
ee.py is the main entrypoint.

```bash
Usage: ee.py [OPTIONS]

Options:
  -t, --target TEXT  Location of files to find. Default '.'
  -i, --input TEXT   CSV-file with time ranges to find.  [required]
  --format TEXT      How to find the time range covered by the file. Valid
                     formats are 'filename' or 'segy'

  --help             Show this message and exit.

```

## Dependencies
 - Decimate - Used to extract given traces from segd files - https://git.equinor.com/sentry/decimate
