from fastapi import FastAPI,WebSocket

class MessageCount:
    managers = []
    receive_manager = []
app = FastAPI()
@app.websocket("/api/")
async def manager(websocket: WebSocket):
    await websocket.accept()
    while True:
        MessageCount.receive_manager.append(await websocket.receive_text())
        if MessageCount.managers :
            for i in MessageCount.managers:
                await websocket.send_text(i)
            MessageCount.managers.clear()