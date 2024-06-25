# scripts/user_app.py
import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
client_id = "user_client"

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("Received message:", data)

client = mqtt_client.Client(client_id)
client.on_message = on_message

if __name__ == "__main__":
    client.connect(broker)
    client.subscribe("lab/leds/state")
    client.loop_forever()

