from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt_client
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

broker = "broker.emqx.io"
mqtt_client_instance = mqtt_client.Client()

subscriptions = {}

@app.on_event("startup")
async def startup_event():
    mqtt_client_instance.connect(broker)
    mqtt_client_instance.loop_start()

@app.on_event("shutdown")
async def shutdown_event():
    mqtt_client_instance.loop_stop()
    mqtt_client_instance.disconnect()

@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    await websocket.accept()
    
    if topic not in subscriptions:
        subscriptions[topic] = []
        mqtt_client_instance.subscribe(topic)
    
    subscriptions[topic].append(websocket)

    while True:
        try:
            data = await websocket.receive_text()
        except:
            subscriptions[topic].remove(websocket)
            if not subscriptions[topic]:
                mqtt_client_instance.unsubscribe(topic)
                del subscriptions[topic]
            break

def on_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')

    if topic in subscriptions:
        websockets = subscriptions[topic]
        for ws in websockets:
            asyncio.run(ws.send_text(payload))

mqtt_client_instance.on_message = on_mqtt_message

