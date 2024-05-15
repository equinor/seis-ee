#! /usr/bin/env bash

set -u

# WATCHDIR="./testwatchdir"
WATCHDIR="/home/earthworm/ew/earthworm_7.10/run/data/web/ewhtmlemail"
MAIL_HEADER="/home/earthworm/ew/earthworm_7.10/run/data/web/ewhtmlemail/em_header.tmp"

echo "Script startet $(date)"

inotifywait -m $WATCHDIR -e create -e moved_to |
    while read dir action file; do
        if [[ "$file" =~ ^(em_).*(.html) ]]; then
            echo "The file '$file' appeared in directory '$dir' via '$action'"
            echo "Sending email with command 'cat $MAIL_HEADER $WATCHDIR/$file | /usr/sbin/sendmail -t'..."
            cat $MAIL_HEADER $WATCHDIR/$file | /usr/sbin/sendmail -t
            if [ $? == 0 ]; then
                echo "INFO: Email sent successfully"
            else
                echo "ERROR: Failed to sent last email"
            fi
            echo "INFO: Watching for new files..."
        fi
    done
