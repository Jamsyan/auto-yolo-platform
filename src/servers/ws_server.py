import asyncio
import json
from typing import Set
from fastapi import FastAPI, WebSocket
active_connections: Set[WebSocket] = set()
app = FastAPI()
message_queue = asyncio.Queue()
@app.post("/api/inside/post/")
async def get_msg(data: dict):
    await message_queue.put(data)

@app.websocket("/api/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        # 创建并发任务
        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))
        await asyncio.wait([receive_task, send_task],return_when=asyncio.FIRST_COMPLETED)
    except Exception as e:
        print(f"WebSocket连接异常: {e}")

async def receive_messages(websocket: WebSocket):
    """接收客户端消息"""
    while True:
        data = await websocket.receive_text()
        await process_feedback_information(data)

async def send_messages(websocket: WebSocket):
    while True:
        try:
            data = await asyncio.wait_for(message_queue.get(), timeout=0.01)
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(0.001)

        except asyncio.TimeoutError:
            # 发送心跳保持连接
            await websocket.send_json({"type": "link:keep"})
            await asyncio.sleep(5)

        except Exception as e:
            print(f"消息发送异常: {e}")
            break

async def process_feedback_information(data):
    print(data)