import time
import paho.mqtt.client as mqtt_client
import random

broker = "broker.emqx.io"
client_id = 'publisher'

def publish_data(topic, data):
    client = mqtt_client.Client(client_id)
    client.connect(broker)
    client.loop_start()

    client.publish(topic, data)

    client.disconnect()
    client.loop_stop()

def simulate_and_publish(satellite):
    while True:
        state = "on" if random.randint(0, 1) == 0 else "off"
        state += satellite
        publish_data("lab/leds/state", state)
        time.sleep(2)

if __name__ == "__main__":
    satellite = "ANTC00CHL"  # Здесь можно сделать параметр для передачи из FastAPI
    simulate_and_publish(satellite)
