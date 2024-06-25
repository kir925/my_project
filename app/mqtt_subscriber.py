import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
client_id = "subscriber-client-id"

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("Received message:", data)

def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.on_message = on_message
    client.connect(broker)
    return client

def subscribe_to_topics(topics):
    client = connect_mqtt()
    client.loop_start()
    for topic in topics:
        client.subscribe(topic)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()

