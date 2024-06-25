# scripts/gnss_daemon.py
import os
import time
import paho.mqtt.client as mqtt_client
from gnss_tec import rnx

broker = "broker.emqx.io"
client_id = "gnss_daemon"

client = mqtt_client.Client(client_id)

def publish_gnss_data(file_path):
    with open(file_path) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            data = {
                "timestamp": tec.timestamp,
                "satellite": tec.satellite,
                "phase_tec": tec.phase_tec,
                "p_range_tec": tec.p_range_tec,
            }
            client.publish("gnss/data", json.dumps(data))
            time.sleep(30)

if __name__ == "__main__":
    gnss_files_dir = "../data/gnss_files"
    for filename in os.listdir(gnss_files_dir):
        if filename.endswith(".rnx"):
            file_path = os.path.join(gnss_files_dir, filename)
            client.connect(broker)
            client.loop_start()
            publish_gnss_data(file_path)

