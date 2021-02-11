#! /usr/bin/env bash
set -euo

RUN_MODE=${RUN_MODE:="decimator"}

if [ "$RUN_MODE" = "decimator" ]; then
    python3 /app/decimator.py
elif [ "$RUN_MODE" = "streamer" ]; then
    python3 /app/streamer.py
elif [ "$RUN_MODE" = "converter" ]; then
    python3 /app/converter.py
else
  exec "$@"
fi
