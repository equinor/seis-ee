
# This script assumes that the azure file storage dev-ccs-passive (located in the ccs storage account on Azure) is mounted to the local folder /archive.


DISK_NAME=/dev/sdc
DISK_PERCENTAGE_USED=$(df -Ph $DISK_NAME | grep -Po '\d+(?=%)')
DISK_PERCENTAGE_LIMIT=80

SERVICES=(ringserver-nnsn link-nnsn slink-norsar)

EQUINOR_FOLDER="/ccs-passive/mseed/equinor"
NNSN_FOLDER="/ccs-passive/mseed/nnsn"
NNSN_EQUINOR_FOLDER="/ccs-passive/mseed/nnsn-equinor"
NORSAR_FOLDER="/ccs-passive/mseed/norsar"

FOLDERS_TO_COPY=($EQUINOR_FOLDER $NNSN_FOLDER $NNSN_EQUINOR_FOLDER $NORSAR_FOLDER)

if [ $DISK_PERCENTAGE_USED -gt $DISK_PERCENTAGE_LIMIT ]
then
    echo "Disk is almost full - moving miniSeed data from local disk to azureFiles."

    # SHUT DOWN STREAM SERVICES
    sudo systemctl stop ${SERVICES[@]}

    # MOVE FILES FROM SDS DISK TO AZURE FILES AND DELETE MSEED FILES FROM /ccs-passive/mseed
    if sudo rsync -a /ccs-passive/mseed /archive/mseed ; then
        rm -r ${FOLDERS_TO_COPY[@]}
    fi

    # RESTART STREAM SERVICES
    sudo systemctl start ${SERVICES[@]}

fi

echo "--- Disk cleanup script finished ---"
