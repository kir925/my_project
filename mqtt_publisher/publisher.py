import time
import paho.mqtt.client as mqtt_client
import random

broker = "broker.emqx.io"
client = mqtt_client.Client('publisher_client_id')

def publish_data(data):
    client.connect(broker)
    client.publish("gnss_data", data)
    client.disconnect()

if __name__ == "__main__":
    client.connect(broker)
    client.loop_start()
    for data in read_rinex_file("rinex_reader/rinex_files/ASCG00SHN_R_20240010000_01D_30S_MO.rnx"):
        publish_data(data)
        time.sleep(30)  # Publish data every 30 seconds
    client.loop_stop()

