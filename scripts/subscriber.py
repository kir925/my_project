# scripts/subscriber.py
import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
client_id = "subscriber_client"

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("Received message:", data)

client = mqtt_client.Client(client_id)
client.on_message = on_message

if __name__ == "__main__":
    client.connect(broker)
    client.subscribe("gnss/data")
    client.loop_forever()

