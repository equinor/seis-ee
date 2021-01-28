
import subprocess
import json
from enum import Enum
from streamer import main

class DecimateFormat(Enum):
    SEGD_GRANE = "segd-grane"
    SU_OSEBERG = "su-oseberg"

if __name__ == '__main__':
    # docker-compose run seis_ee stream-files -t /data -s /data/nodes.csv
    target_path: str = "/data"
    sensor_list_path: str = "/data/nodes.csv"
    format: str = "su-oseberg"  #"segd-grane"
    destination = "/data/opt/project/seis_ee/decimated_files/2021/1"
    #conf_string = {"name": "ccs", "format": "su-oseberg", "description": "30 nodes from oseberg for CCS", "included_nodenames": [102, 261, 368]}

    nodes = [102, 261, 368] #[12, 21, 28, 31, 33, 40, 48, 50, 53, 57, 62, 64, 66, 95, 105]
    conf = {
        "name": "ccs",
        "format": DecimateFormat.SU_OSEBERG.value,
        "description": "30 nodes from oseberg for CCS",
        "included_nodenames": nodes
    }
    conf_string = json.dumps(conf)
    file_path = "/data/OsebergC-SWIM_01/su_files/Passive_20210127_000001/production/514992.su"
    #try:
    #    subprocess.run(args=f"ssh {Config.stream_server_user}@{Config.stream_server_host} mkdir -p {path}",
    #                                      shell=True, check=True, capture_output=True, encoding="UTF-8")
    main(target_path, sensor_list_path, format)
    print("TEST")