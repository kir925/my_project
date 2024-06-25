import time
import paho.mqtt.client as mqtt_client
from gnss_tec import rnx
import os
import sys

broker = "broker.emqx.io"
topic_prefix = "lab/gnss/"
interval = 30  # Периодичность публикации данных

def publish_data(file_path):
    client = mqtt_client.Client(f'publisher_{os.path.basename(file_path)}')
    client.connect(broker)
    client.loop_start()

    topic = f"{topic_prefix}{os.path.basename(file_path)}"
    
    with open(file_path) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            message = f"{tec.timestamp} {tec.satellite} {tec.phase_tec} {tec.p_range_tec}"
            client.publish(topic, message)
            time.sleep(interval)  # Публикация каждые 30 секунд

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    file_path = sys.argv[1]
    publish_data(file_path)

