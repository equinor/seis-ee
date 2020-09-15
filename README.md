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


## How-to extract data from Grane

1. Get a file with a series of time-ranges in ISO8012(confirm this) format
TODO: Remove first column

```text
2020-07-28T11:59:44 2020-07-28T11:59:30 2020-07-28T11:59:59
2020-07-28T11:59:44 2020-07-28T11:59:30 2020-07-28T11:59:59
2020-07-28T11:59:44 2020-07-28T11:59:30 2020-07-28T11:59:59
```

2. (Optional) If you only need data from a subset of nodes, create a list of the nodes you need
TODO: How to create nodeName/nodeNumber(?!) 
```text
nodeName,nodeNo
10357,102
20383,261
30351,368
```

3. Seis-EE and it's notable dependencies (segyIO, Decimate) is packaged with Docker. The easiest way to run it is with the provided docker-compose-file.  
Update it so the location of the raw-files (often a network share of several TB's/PB's) are mounted into the containers `/raw`-directory.
4. Run each of these commands manually, and confirm the correctness of the results between.

```bash
docker-compose run seis_ee find-files --target /raw --input /data/requested-times.txt --format filename
docker-compose run seis_ee reduce-files --file-list raw-result.txt --sensor-list sensors.txt --format segd-grane
```

5. Done! Your final files should now be in `./decimated-files/`
