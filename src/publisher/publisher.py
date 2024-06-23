import paho.mqtt.client as mqtt
from gnss_tec import rnx

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("rinex/data")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    # Process RINEX data
    with open('path_to_rinex_file.rnx') as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            print(
                '{} {}: {} {}'.format(
                    tec.timestamp,
                    tec.satellite,
                    tec.phase_tec,
                    tec.p_range_tec,
                )
            )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-broker", 1883, 60)
client.loop_forever()

