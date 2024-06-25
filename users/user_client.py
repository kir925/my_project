import requests
import time
import paho.mqtt.client as mqtt_client

API_URL = "http://localhost:8000"

def get_available_topics():
    response = requests.get(f"{API_URL}/topics")
    return response.json().get("topics", [])

def on_message(client, userdata, message):
    print(f"Received message from topic {message.topic}: {message.payload.decode('utf-8')}")

def subscribe_to_topics(topics):
    client = mqtt_client.Client(f"user_client_{int(time.time())}")
    client.on_message = on_message

    broker = "broker.emqx.io"
    client.connect(broker)
    client.loop_start()

    for topic in topics:
        client.subscribe(f"lab/gnss/{topic}")
        print(f"Subscribed to topic: {topic}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    available_topics
