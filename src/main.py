# -*- coding: utf-8 -*-
import json
import logging
import asyncio
from uvicorn import run
from fastapi import FastAPI,WebSocket
from auto_annotation import VideoFrameExtractor
from api.managers import Message,messages
from concurrent.futures import ThreadPoolExecutor

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='logs/log.log')

def workflow():
    video = VideoFrameExtractor()
    video.execute()
app = FastAPI()
@app.websocket("/api/")
async def main(websocket:WebSocket):
    await websocket.accept()
    executer = ThreadPoolExecutor(max_workers=5)
    executer.submit(workflow)
    while True:
        if messages:
            for data in messages:
                await asyncio.sleep(0.1)
                await websocket.send_text(json.dumps(data))
                print(data)
            messages.clear()

if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000, log_level="info")