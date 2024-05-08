from fastapi import FastAPI, WebSocket
from typing import List
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware
import configparser 
from settings import Options
import logging
import MessagesManager
import pprint

printer = pprint.PrettyPrinter(indent=12, width=120)
prnt = printer.pprint

options = Options(Path(os.path.abspath(os.curdir)).parent / "options.ini")

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=['*'], 
	allow_headers=["*"]
)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

# Список активных подключений
active_connections = []

MessangerManager = MessagesManager.MessageManager(      
		options.Messages_databaseUri,
		options.Messages_Database,
		options.Messages_Collection    )

class SiteRequest:
	def __init__(self, username:str, command:str, comment:str, data:str):
		self.username = username
		self.command = command
		self.comment = comment
		self.data = data


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)  # Добавляем новое подключение в список
    try:
        while True:
            data = await websocket.receive_text()
            site_request = SiteRequest(**json.loads(data))
            if site_request.command == "GetMessagesLast":
                result = MessangerManager.get_last_messages(username=site_request.username, num_messages=int(site_request.data))
                await websocket.send_json(result)
            elif site_request.command == "AddMessage":
                result = MessangerManager.save_message(username=site_request.username,
                                                        message_text=site_request.data,
                                                        icon_name=site_request.comment,
                                                        hyperlink=site_request.command)
                await websocket.send_json(result)
    finally:
        active_connections.remove(websocket)  # Удаляем закрытое подключение из списка


# Функция для отправки сообщения всем активным подключениям
async def send_message_to_all(message):
    for connection in active_connections:
        await connection.send_json(message)