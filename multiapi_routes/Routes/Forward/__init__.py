import os
import asyncio
import logging
import threading

from typing import Any, Dict
from dotenv import load_dotenv

from vauth import login , VAuth

from celery import Celery

from fastapi import WebSocket

from fastapi import APIRouter, WebSocket ,Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect

from multiapi_routes.Routes.VirtualBond import Virtual_Bond

load_dotenv()

bk = os.environ['CELERY_BROKER_URL']

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
        self.vb = Virtual_Bond()

    async def connect(self, websocket: WebSocket,model_id : str, token: str):
        """connect event"""
        await websocket.accept()
        try:
            token = login(token)
            
            vb = self.vb.read_items(token=token,id=model_id)
            #print(vb.status)
            if vb.status == "error":
                raise HTTPException(status_code=404, detail=vb.error)
            #print(vb)
            self.active_connections.append(websocket)
            await websocket.send_json({"status":"success","result":"Connected"})
            return token
        except HTTPException as e:
            print("HTTPException:",e)
            await websocket.send_json({"status":"error","result":str(e.detail)})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
        except Exception as e:
            print("Exception:",e)
            await websocket.send_json({"status":"error","result":str(e)})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

    async def return_task(self, output: Any, websocket: WebSocket):
        """Direct Message"""
        await websocket.send(output)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)

class forward(APIRouter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "froward"
        bk = os.environ['CELERY_BROKER_URL']
        self.vb = Virtual_Bond()
        if bk is None:
            raise HTTPException(status_code=404, detail="No CELERY_BROKER_URL Found")
        self.celery = Celery('tasks', broker=bk, backend=bk)
        self.add_api_route("/forward", self.create_item, methods=["POST"], dependencies=[Depends(login)])
        self.add_api_route("/forward", self.Websocket_Example, methods=["GET"])
    
    def create_item(self,model : str,arg : Dict , token: str = Depends(login)):
        self.vb.read_items(token=token,id=model)
        task = self.celery.send_task('multiapi.brain_task', args=(model, token.token, arg))
        print(task.id)
        while task.status != "SUCCESS":
            print(task.status,end="\r")
        return task.get()

    def Websocket_Example(self):
        template = open("html/websocket_client.html","r").read()
        return HTMLResponse(template)

forward_ = forward()

@forward_.websocket("/{model_id}/stream")
async def websocket_endpoint(websocket: WebSocket, model_id: str, token: str = Query(None)):
    forward_manager = ConnectionManager()
    celery = Celery('tasks', broker=bk, backend=bk)
    token = await forward_manager.connect(websocket, model_id, token)
    if token is not None:
        # Queue
        tasks = asyncio.Queue()
        async def rcv(websocket: WebSocket = websocket):
            while True:
                try:
                    data = await websocket.receive()
                    logging.info("Received: %s", data)
                    if data["type"] == "websocket.disconnect":
                        await websocket.send_json({"status":"success","result":"Disconnected"})
                        forward_manager.disconnect(websocket)
                        break
                    elif data:
                        input_data = None
                        logging.info("Adding Task %s", input_data)
                        task = celery.send_task('multiapi.brain_task', args=(model_id, token.token, data))
                        await tasks.put(task)
                        logging.info("Task Added")
                        await websocket.send_json({"status":"success","result":"Task Added"})
                except WebSocketDisconnect as e:
                    logging.error("WebSocket Error: %s", e)
                    forward_manager.disconnect(websocket)
                    break

        async def send():
            while True:
                try:
                    task = await tasks.get()
                    logging.info(task.id)
                    while task.status != "SUCCESS":
                        logging.info(task.status, end="\r")
                        await asyncio.sleep(0.001)
                    logging.info(task.status)
                    info = task.result
                    logging.info(info)
                    logging.info("Task Info %s", info)
                    await websocket.send_json(info)
                    logging.info("Task Sent")
                except WebSocketDisconnect as e:
                    logging.error("WebSocket Error: %s", e)
                    forward_manager.disconnect(websocket)
                    break
                except Exception as e:
                    logging.error(e)
                    pass
        await asyncio.gather(send(), rcv())