import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("received message =", data)

client = mqtt_client.Client('subscriber_client')
client.on_message = on_message

print("Connecting to broker", broker)
client.connect(broker)
client.loop_start()

print("Subscribing to topic")
client.subscribe("lab/gnss/#")  # Подписка на все топики с префиксом "lab/gnss/"

# Работать в течение 30 минут (1800 секунд)
time.sleep(1800)
client.disconnect()
client.loop_stop()

