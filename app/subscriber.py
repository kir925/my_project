import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
topic = "gnss/data"

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("received message =", data)

client = mqtt_client.Client()
client.on_message = on_message

print("Connecting to broker", broker)
client.connect(broker)
client.loop_start()
print("Subscribing to topic", topic)
client.subscribe(topic)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()

