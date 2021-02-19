#! /usr/bin/env bash
set -euo

RUN_MODE=${RUN_MODE:="decimator"}

if [ "$RUN_MODE" = "decimator" ]; then
    python3 /app/event_listener.py
elif [ "$RUN_MODE" = "converter" ]; then
    python3 /app/mseed_converter.py
elif [ "$RUN_MODE" = "test" ]; then
    behave /app/tests/features/
else
  exec "$@"
fi
