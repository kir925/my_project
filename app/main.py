from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

available_topics = ["receiver_1", "receiver_2", "receiver_3"]

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket GNSS Data</title>
    </head>
    <body>
        <h1>GNSS Data Stream</h1>
        <ul id='messages'>
        </ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/topics")
async def get_topics():
    return {"topics": available_topics}

@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    await websocket.accept()
    if topic not in available_topics:
        await websocket.close(code=1003)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        pass
