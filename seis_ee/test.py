
import subprocess
import json
from enum import Enum
from streamer import main

class DecimateFormat(Enum):
    SEGD_GRANE = "segd-grane"
    SU_OSEBERG = "su-oseberg"

if __name__ == '__main__':
    target_path: str = "/data"
    sensor_list_path: str = "/data/nodes.csv"
    format: str = "su-oseberg"  #"segd-grane"

    main(target_path, sensor_list_path, format)