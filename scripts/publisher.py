# scripts/publisher.py
import time
import paho.mqtt.client as mqtt_client
import random

broker = "broker.emqx.io"
client_id = "publisher_client"

client = mqtt_client.Client(client_id)

print(f"Connecting to broker: {broker}")
client.connect(broker)
client.loop_start()

for i in range(10):
    state = "on" if random.randint(0, 1) == 0 else "off"
    state = state + " ArtemV"
    print(f"Publishing state: {state}")
    client.publish("lab/leds/state", state)
    time.sleep(2)

client.disconnect()
client.loop_stop()

