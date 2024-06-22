import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
client_id = 'subscriber'

def on_message(client, userdata, message):
    data = message.payload.decode("utf-8")
    print("Received message:", data)

def subscribe_to_mqtt():
    client = mqtt_client.Client(client_id)
    client.on_message = on_message

    client.connect(broker)
    client.subscribe("lab/leds/state")
    client.loop_forever()

if __name__ == "__main__":
    subscribe_to_mqtt()

