import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
client = mqtt_client.Client('subscriber_client_id')

def on_message(client, userdata, message):
    data = message.payload.decode("utf-8")
    print(f"Received message: {data}")

if __name__ == "__main__":
    client.connect(broker)
    client.on_message = on_message
    client.subscribe("gnss_data")
    client.loop_forever()

