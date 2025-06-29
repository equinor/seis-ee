#! /usr/bin/env bash
#set -euox pipefail
DISK_NAME=/dev/sda
DISK_PERCENTAGE_USED=$(df -Ph $DISK_NAME | grep -Po '\d+(?=%)')
DISK_PERCENTAGE_LIMIT=80
LOG_FILES_DIR=/data/ew/earthworm_7.10/run/log

SERVICES=(earthworm seiscomp)
echo "Disk percentage used: ${DISK_PERCENTAGE_USED}"
if [ $DISK_PERCENTAGE_USED -gt $DISK_PERCENTAGE_LIMIT ]
then
echo "Disk is almost full - moving data from folder /data/archive from local disk to azureFiles (/archive folder)."

# SHUT DOWN STREAM SERVICES
sudo systemctl stop ${SERVICES[@]}

# MOVE FILES FROM SDS DISK TO AZURE FILES AND DELETE MSEED FILES FROM /ccs-passive/mseed
sudo rsync --remove-source-files -a /data/archive /archive

# RESTART STREAM SERVICES
sudo systemctl start ${SERVICES[@]}

fi

# Remove log files older than 10 days
find "$LOG_FILES_DIR" -mtime +5 -type f -delete
# Remove earthworm startstop logs(They can grow huge...)
rm -rf /data/ew/logs/startstop.log
rm -rf /data/ew/logs/startstop_error.log
