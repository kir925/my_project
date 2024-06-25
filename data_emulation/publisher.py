import time
import paho.mqtt.client as mqtt_client
from gnss_tec import rnx  # Подставьте свой модуль или библиотеку для чтения rnx файлов

broker = "broker.emqx.io"
topic = "lab/gnss/data"

client = mqtt_client.Client('gnss_publisher')
client.connect(broker)
client.loop_start()

def publish_data(file_path):
    with open(file_path) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            message = f"{tec.timestamp} {tec.satellite} {tec.phase_tec} {tec.p_range_tec}"
            client.publish(topic, message)
            time.sleep(30)  # публикуем каждые 30 секунд

if __name__ == "__main__":
    publish_data('example.rnx')  # Пример файла .rnx для публикации
    client.loop_stop()
    client.disconnect()
