# fastapi_server/main.py
from fastapi import FastAPI
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
client_id = "fastapi_server"

app = FastAPI()
client = mqtt_client.Client(client_id)

@app.post("/subscribe/")
async def subscribe_to_satellite(satellite_name: str):
    topic = f"gnss/{satellite_name}"
    client.connect(broker)
    client.subscribe(topic)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

