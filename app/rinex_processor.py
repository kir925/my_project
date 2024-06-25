import os
import time
import json
from gnss_tec import rnx
import paho.mqtt.client as mqtt_client
from multiprocessing import Process

from app.mqtt_publisher import connect_mqtt, publish_data

def read_rinex_file(file_path):
    with open(file_path) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            yield {
                'timestamp': tec.timestamp,
                'satellite': tec.satellite,
                'phase_tec': tec.phase_tec,
                'p_range_tec': tec.p_range_tec,
            }

def process_rinex_file(file_path, client_id):
    client = connect_mqtt(client_id)
    client.loop_start()
    topic = f"gnss/{os.path.basename(file_path)}"

    for data in read_rinex_file(file_path):
        publish_data(client, topic, data)
        time.sleep(30)

    client.disconnect()
    client.loop_stop()

def start_daemons(rinex_files):
    processes = []
    for file_path in rinex_files:
        client_id = f"publisher-{os.path.basename(file_path)}"
        p = Process(target=process_rinex_file, args=(file_path, client_id))
        p.daemon = True
        p.start()
        processes.append(p)
    return processes

