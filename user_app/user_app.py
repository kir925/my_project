import time

def process_data(data):
    print(f"Processed data: {data}")

if __name__ == "__main__":
    from mqtt_subscriber.subscriber import on_message
    
    # Simulate receiving data from MQTT subscriber
    on_message(None, None, b"Sample data from subscriber")
    time.sleep(2)

