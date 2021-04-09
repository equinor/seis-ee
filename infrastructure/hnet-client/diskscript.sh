
# This script assumes that the azure file storage dev-ccs-passive (located in the ccs storage account on Azure) is mounted to the local folder /archive.


DISK_NAME=/dev/sdc
DISK_PERCENTAGE_USED=$(df -Ph $DISK_NAME | grep -Po '\d+(?=%)')
DISK_PERCENTAGE_LIMIT=80

SERVICES=(ringserver-nnsn link-nnsn slink-norsar)

if [ $DISK_PERCENTAGE_USED -gt $DISK_PERCENTAGE_LIMIT ]
then
    echo "Disk is almost full - moving miniSeed data from local disk to azureFiles."

    # SHUT DOWN STREAM SERVICES
    sudo systemctl stop ${SERVICES[@]}

    # MOVE FILES FROM SDS DISK TO AZURE FILES AND DELETE MSEED FILES FROM /ccs-passive/mseed
    sudo rsync --remove-source-files -a /ccs-passive/mseed /archive/mseed

    # RESTART STREAM SERVICES
    sudo systemctl start ${SERVICES[@]}

fi

echo "--- Disk cleanup script finished ---"
