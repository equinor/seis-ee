#! /usr/bin/env bash
set -euo

RUN_MODE=${RUN_MODE:="decimator"}
echo "$@"
if [ "$1" = "start" ]; then
  if [ "$RUN_MODE" = "decimator" ]; then
      python3 /app/event_listener.py
  elif [ "$RUN_MODE" = "converter" ]; then
      python3 /app/mseed_converter.py
fi
else
  exec "$@"
fi
