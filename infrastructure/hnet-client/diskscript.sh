DISK_NAME=/dev/sdc
DISK_PERCENTAGE_USED=$(df -Ph $DISK_NAME | grep -Po '\d+(?=%)')
DISK_PERCENTAGE_LIMIT=80

RINGSERVER_SERVICE=ringserver-nnsn.service
SLINK_NNSN_SERVICE=slink-nnsn.service
SLINK_NORSAR_SERVICE=slink-norsar.service

SAS_TOKEN="GET_FROM_AZURE..."

EQUINOR_FOLDER="/ccs-passive/mseed/equinor"
NNSN_FOLDER="/ccs-passive/mseed/nnsn"
NNSN_EQUINOR_FOLDER="/ccs-passive/mseed/nnsn-equinor"
NORSAR_FOLDER="/ccs-passive/mseed/norsar"

FOLDERS_TO_COPY=($EQUINOR_FOLDER $NNSN_FOLDER $NNSN_EQUINOR_FOLDER $NORSAR_FOLDER)

if [ $DISK_PERCENTAGE_USED -gt $DISK_PERCENTAGE_LIMIT ]
then
    echo "Disk is almost full - move files from ccs-passive to azure."

    # SHUT DOWN STREAM SERVICES
    sudo systemctl stop $RINGSERVER_SERVICE $SLINK_NNSN_SERVICE $SLINK_NORSAR_SERVICE

    # MOVE FILES FROM SDS DISK TO AZURE FILE STORAGE
    for folder in "${FOLDERS_TO_COPY[@]}"
    do
        echo $folder
        if sudo azcopy copy $folder "https://ccs.file.core.windows.net/prod-ccs-passive/ccs-passive$SAS_TOKEN" --recursive ; then
            rm -r $folder
        else
            echo "ERROR: could not folder $folder to Azure..."
        fi
    done

    # RESTART STREAM SERVICES
    sudo systemctl start $RINGSERVER_SERVICE $SLINK_NNSN_SERVICE $SLINK_NORSAR_SERVICE

fi

echo "--- Disk cleanup script finished ---"
