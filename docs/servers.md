# HNET server

The HNET server is hosted as a VM in Azure (HNET resource group in S155-Background_Seis subscription).

## Disk cleanup

Currently, the streamed data is stored in the folder /ccs-passive in HNET. The disk used for this data has a capacity of 2 TB. A disk cleanup script (infrastucture/hnet-client/diskscript.sh.) will

1. stop streaming services.
2. copy the files from the folder /ccs-passive to Azure file storage
3. delete data from /ccs-passive
4. start streaming services

The Azure file share "dev-ccs-passive" is mounted to the folder /archive on the HNET server.

A disk cleanup script will be run once per week (the script can be found in infrastucture/hnet-client/diskscript.sh).

## Cron jobs

Every saturday at 01.00, the VM is automatically rebooted to apply security upgrades from unattended upgrades.
This is defined in the file /etc/crontab.

Also, the disk cleanup script will every saturday at 04.00.

# EARTHWORM server

The EARTHWORM server is hosted as a VM in Azure (EarthWorm resource group in S155-Background_Seis subscription).

## Disk cleanup

A similar disk cleanup script (script can be found in the folder infrastucture/earthworm/diskscript.sh on github) is used as for the HNET server. This will stop the earthworm and seiscomp services, move the files in /data/archive to /archive and restart the serviecs.

/archive folder on the Earthworm VM is a mounted file share "earthworm" from azure filestorage (this is defined in /etc/fstab). This Azure file storage is found in the CCS resources group in S155-Background_Seis subscription.

## Cron jobs

Every saturday at 01.00, the VM is automatically rebooted to apply security upgrades. Also, the disk cleanup script will every saturday at 04.00.

# EARTHWORM 2 server

TODO?
