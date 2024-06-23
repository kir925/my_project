import paho.mqtt.client as mqtt
import os
import time
from gnss_tec import rnx

# MQTT настройки
broker = "mqtt-broker"
port = 1883
topic = "rinex_data"

def on_publish(client, userdata, result):
    print("Данные опубликованы \n")
    pass

client = mqtt.Client()
client.on_publish = on_publish
client.connect(broker, port)

rinex_dir = "/data_downloader"
for root, dirs, files in os.walk(rinex_dir):
    for file in files:
        if file.endswith(".rnx"):
            file_path = os.path.join(root, file)
            with open(file_path) as obs_file:
                reader = rnx(obs_file)
                for tec in reader:
                    message = f"{tec.timestamp} {tec.satellite}: {tec.phase_tec} {tec.p_range_tec}"
                    client.publish(topic, message)
                    time.sleep(1)
