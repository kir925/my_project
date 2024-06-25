import json
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"

def connect_mqtt(client_id):
    client = mqtt_client.Client(client_id)
    client.connect(broker)
    return client

def publish_data(client, topic, data):
    result = client.publish(topic, json.dumps(data))
    status = result[0]
    if status != 0:
        print(f"Failed to send message to topic {topic}")

