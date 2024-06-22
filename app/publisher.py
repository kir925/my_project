import time
import paho.mqtt.client as mqtt_client
from gnss_tec import rnx

broker = "broker.emqx.io"
topic = "gnss/data"

def start_publishing(satellite):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker)
    client.loop_start()

    with open(f'data/{satellite}_R_20241680000_01D_30S_MO.rnx') as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            message = f'{tec.timestamp} {tec.satellite}: {tec.phase_tec} {tec.p_range_tec}'
            print(f"Publishing: {message}")
            client.publish(topic, message)
            time.sleep(2)  # Задержка между сообщениями

    client.loop_stop()
    client.disconnect()

