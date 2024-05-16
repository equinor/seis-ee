#! /usr/bin/env bash

set -u

# WATCHDIR="./testwatchdir"
WATCHDIR="/home/earthworm/ew/earthworm_7.10/run/data/web/ewhtmlemail"
MAIL_HEADER="/home/earthworm/ew/earthworm_7.10/run/data/web/ewhtmlemail/em_header.tmp"

log_prefix() {
    LEVEL=${1:-"INFO"}
    echo "$(date --rfc-3339 s) - $LEVEL:"
}

trap "echo '$(log_prefix)  Shutting down...'" EXIT

echo "$(log_prefix) Script startet"

inotifywait -m $WATCHDIR -e create -e moved_to |
    while read dir action file; do
        if [[ "$file" =~ ^(em_).*(.html) ]]; then
            echo "$(log_prefix) The file '$file' appeared in directory '$dir' via '$action'"
            echo "$(log_prefix) Sending email with command 'cat $MAIL_HEADER $WATCHDIR/$file | /usr/sbin/sendmail -t'..."
            cat $MAIL_HEADER $WATCHDIR/$file | /usr/sbin/sendmail -t
            if [ $? == 0 ]; then
                echo "$(log_prefix) Email sent successfully"
            else
                echo "$(log_prefix 'ERROR') Failed to sent last email"
            fi
            echo "$(log_prefix) Watching for new files..."
        fi
    done
