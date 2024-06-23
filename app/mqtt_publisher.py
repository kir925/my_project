import threading
import paho.mqtt.publish as publish
from gnss_tec import rnx

def start_publisher(file_path: Path, satellite: str):
    def publish_data():
        with open(file_path, 'r') as obs_file:
            reader = rnx(obs_file)
            for tec in reader:
                data = {
                    'timestamp': str(tec.timestamp),
                    'satellite': tec.satellite,
                    'phase_tec': tec.phase_tec,
                    'p_range_tec': tec.p_range_tec,
                }
                publish.single("gnss/tec", payload=str(data), hostname="broker.hivemq.com")

    thread = threading.Thread(target=publish_data)
    thread.start()

