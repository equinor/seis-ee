# CCS-passive Runbook

This document covers information about how the solution works and information for developers.

![Diagram](architecture.drawio.svg)


1. The data source (Azure blob storage) - The offshore operators upload raw seismic data near real-time. Currently, data from offshore fileds Snorre, Grane and Oseberg is collected.
2. The Azure Storage Account is configured to send an HTTP post request on creation of new blobs (a blob is created whenever a new seismic file appears in the Azure storage). Azure event grid is used for sending this request to out API endpoint. 
3. A Python FastAPI web server running in Omnia Radix. This API is listening for events (http POST requests). When a new event occurs (containing the filename of the newly created seismic file), the newly created seismic file is pulled from the azure blob storage (1) and the file is decimated. Afterwards, the decimated fils is uploaded toto CCS-Passive's Azure File Storage. 
4. A message is added to the Convert Queue when a new file has been decimated. This message contains the seismic file type and the path to the decimated file in the Azure file storage.
5. A python wrapper for a C++ program that downloads decimated files from Azure file storage, covert them to miniSeed (mseed) format, and uploads them to the File Share.
6. A Ubuntu virtual machine running SeisComp's seedlinktool to stream miniseed data both up and down.
7. Data to external networks are streamed via seedlink through a Wireguard VPN tunnel.
8. (Out of scope) Equinor consumers of the data can connect to the seedlink server.


## CI/CD
The Continous Integration is set up using Github Actions, and the configuration can be found in the GitHub/workflows folder. When new changes are pushed to the master branch, the following steps are performed:
1. Testing
2. Build and push a docker image to the github docker registry
3. Deploy the application to Omnia Radix

## Omnia Radix
The application is hosted in [Omnia Radix](https://www.radix.equinor.com). The configuration for the application is defined in the [radixconfig.yaml](./radixconfig.yaml) file. 

## Azure resources

TODO: write something about the common azure storage for seismic files.
subscriptions, resource groups, 

### Event Grid


### Azure Queue 

### Azure FIle Storage


## Developer information

### Running locally

#### Poetry

To run locally, you need the poetry package manager. in the root project folder, run the following command to install python packages:
```sh
poetry install
```
#### Docker

To run the application, Docker and Docker-compose is used. In the root project folder, run the commands
```sh
docker-compose build
docker-compose run
```

The [Docker image](./Dockerfile) depends on the [Sentry/decimate](https://git.equinor.com/sentry/decimate) docker image. You must have access to this docker image before running the ccs-passive application.

#### Environment variables
TODO

#### 


