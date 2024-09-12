# CCS-passive Runbook

This document covers information about how the solution works and information for developers.

![Diagram](architecture.drawio.svg)


1. The data source (Azure blob storage) - The offshore operators upload raw seismic data near real-time. Currently, data from offshore fileds Snorre, Grane and Oseberg is collected.
2. The Azure Storage Account is configured to send an HTTP post request on creation of new blobs (a blob is created whenever a new seismic file appears in the Azure storage). Azure event grid is used for sending this request to out API endpoint. 
3. A Python FastAPI web server running in Omnia Radix. This API is listening for events (http POST requests). When a new event occurs (containing the filename of the newly created seismic file), the newly created seismic file is pulled from the azure blob storage (1) and the file is decimated. Afterwards, the decimated fils is uploaded toto CCS-Passive's Azure File Storage. 
4. A message is added to the Convert Queue when a new file has been decimated. This message contains the seismic file type and the path to the decimated file in the Azure file storage.
5. A python wrapper for a C++ program that downloads decimated files from Azure file storage, covert them to miniSeed (mseed) format, and uploads them to the File Share. The mseed converter is developed by [NNSN](https://www.uib.no/en/rg/geophysics/55876/nnsn).
6. A Ubuntu virtual machine running SeisComp's seedlinktool to stream miniseed data both up and down.
7. Data to external networks are streamed via seedlink through a Wireguard VPN tunnel.
8. (Out of scope) Equinor consumers of the data can connect to the seedlink server.


## CI/CD
The Continous Integration is set up using Github Actions, and the configuration can be found in the [GitHub/workflows](./.github/workflows) folder. When new changes are pushed to the master branch, the following steps are performed:
1. Run tests
2. Build and push a docker image to the github docker registry
3. Deploy the application to Omnia Radix

## Omnia Radix
The application is hosted in [Omnia Radix](https://www.radix.equinor.com) in the ccs-passive application. The configuration for the application is defined in the [radixconfig.yaml](./radixconfig.yaml) file. 
The API endpoint can be found at the url: [www.ccs-passive.app.radix.equinor.com ](ccs-passive.app.radix.equinor.com).

## Azure resources

The Azure resources are located in two different subscritpions: one for the common seismic file storage, and one for ccs-passive components.

### CCS passive resources
These components can be found in subscription: "S155-Background_Seis", inside the Resource group "CCS".

#### Azure storage account: ccs
Used for storing decimated files in the file storage and messages in the queue service.

#### 


## Common stuff.... todo....



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

To run the application, Docker and Docker-compose are used. In the root project folder, run the commands
```sh
docker-compose build
docker-compose run
```

The [Docker image](./Dockerfile) depends on the [Sentry/decimate](https://git.equinor.com/sentry/decimate) docker image. 
You must have access to the decimate repo before you can get access to the docker image. Access to the repo can be given by one of 
the admings on the decimate project.

The application consists of two services in the [docker-compose file](./docker-compose.yaml). The "decimator" is responsible for listening for POST events, 
and the converter polls the azure storage queues and converts decimated files to mseed when new files arrive.

#### Run tests
Two kinds of tests are included in the project: [unit tests](https://docs.python.org/3/library/unittest.html) and [behave tests](https://behave.readthedocs.io/en/stable/). 
These tests will run when pushing new changes to the repo, but can be run locally by using the commands:
```sh
docker-compose run decimator pytest -v

docker-compose run decimator behave
```

#### Pre-commit
It is recommended to install [pre-commit](https://pre-commit.com/) on your computer. Pre-commit can be used for automatic formatting of code and running tests. 
```sh
pre-commit run --all-files
```



#### Environment variables
For local development, the environment variables need to be stored in the .env file in the root folder. A template is found in  [.env-template](./.env-template).
The value for "FILES_CONN_STRING" and "QUEUE_CONN_STRING" can be found in the Azure portal, in the ccs storage account (resource group: CCS, subscription: S155-Background_Seis ) under "Access keys".
The values for BLOB_CONN_STRING can be found in ????? TODO.


TODO: secret for endpoint???


