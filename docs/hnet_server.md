# HNET server

The HNET server is hosted as a VM in Azure.


## Disk cleanup

Currently, the streamed data is stored in the folder /ccs-passive in HNET. The disk used for this data has a capacity of 2 TB. A disk cleanup script (infrastucture/hnet-client/create_azure_file_mount.sh.) will
1) stop streaming services.
2) copy the files from the folder /ccs-passive to Azure file storage
3) delete data from /ccs-passive
4) start streaming services

The Azure file share "dev-ccs-passive" is mounted to the folder /archive on the HNET server.


## Disk cleanup 

A disk cleanup script will be run once per week (the script can be found in infrastucture/hnet-client/diskscript.sh).

## Cron jobs
Every saturday at 04.00, the VM is automatically rebooted to apply security upgrades from unattended upgrades.
This is defined in the file /etc/crontab.

Also, the disk cleanup script will every saturday at 01.00.