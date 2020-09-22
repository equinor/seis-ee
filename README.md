# Seis-EE
_Seismic data event extractor_

## What is Seis-EE
Seis-EE simplifies the process of extracting seismic data from a ranges of dates and times, and a subset of sensor nodes. Useful for looking closer at some seismic events, where time and place is some what limited and known.

## Quick Start
seis_ee.py is the main entrypoint.

```bash
Usage: seis_ee.py [OPTIONS] COMMAND [ARGS]...

Options:
  -l, --log-level [info|warning|error]
                                  Log level. One of 'info', 'warning', 'error'
  --help                          Show this message and exit.

Commands:
  find-files
  reduce-files
```

Find files command
```bash
Usage: seis_ee.py find-files [OPTIONS]

Options:
  -t, --target TEXT              Location of files to find. Default '.'
  -e, --events TEXT              CSV-file with time ranges for the events to
                                 find. Headers (event, from, to). Datetime as
                                 ISO 8601  [required]

  --format [filename|su-header]  How to find the time range covered by the
                                 file. Valid formats are ['filename', 'su-
                                 header']

  --help                         Show this message and exit.
```

Reduce (decimate) files command
```bash
Usage: seis_ee.py reduce-files [OPTIONS]

Options:
  -f, --file-list TEXT            Path to a file containing files to reduce.
                                  As produced by 'seis_ee.py find-files'

  -s, --sensor-list TEXT          Path to a CSV-file containing the sensors to
                                  keep. Headers (nodeName, nodeNo)

  --format [segd-grane|su-oseberg]
                                  Format of the files to reduce. One of
                                  ['segd-grane', 'su-oseberg']

  --help                          Show this message and exit.
```

## Notable Dependencies
 - Decimate - Used to extract given traces from segd files - https://git.equinor.com/sentry/decimate
 - Segyio - Used for reading su-files headers - https://github.com/equinor/segyio


## How-to extract data

1. Get a file with a series of time-ranges in ISO-8601 format

    ```csv
    event from to
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

3. Seis-EE and all it's dependencies is packaged with Docker. The easiest way to run it is with the provided docker-compose-file.  
    Update it so the location of the seismic files are mounted into the containers `/raw`-directory.
4. Run each of these commands manually, and confirm the correctness of the results between.

    ```bash
    docker-compose run seis_ee find-files --target /raw --input /data/requested-times.txt --format filename
    docker-compose run seis_ee reduce-files --file-list raw-result.txt --sensor-list sensors.txt --format segd-grane
    ```

5. Done! Your final files should now be in `./decimated-files/`

## Limitations

- Can only decimate grane and oseberg formated segy/su files
- Can only find files in '--format filename' matching `2020-08-13-14-02-14-Grane2321913.sgd` 
- Can only find files in '--format su-header' matching `/raw/OsebergC-SWIM_06/su_files/Passive_20200602_000000/production/252565.su`  (entire path must match structure)

### Performance

For finding files in `/project/grane-passive` (format filename), we iterate over every file in the file system. Could be a good idea to do one subfolder at a time.

For finding files in `/project/OsebergC-SWIM_XX` (format su-header), we fetch only the files needed, based on requested times. You can safely do this on the whole of `/project/` at once.  
Decimating about 390 files with a 10 sec time span each from oseberg took about 40min.


## TODO

- [ ] Support snorre type SensorTypes (decimate)
- [ ] Investigate missing files. Bad transfer offshore?
