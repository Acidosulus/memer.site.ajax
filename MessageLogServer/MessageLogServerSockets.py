from fastapi import FastAPI, WebSocket
from typing import List
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware
from settings import Options
import logging
import MessagesManager
import pprint
import rich
import json
import subprocess
import time

rich.print({'server':'Sockets server'})

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


init_without_error = True
next_try_delay = 5
try:
	while init_without_error:
		try:
			print('Try to connect to MongoDB')
			MessangerManager = MessagesManager.MessageManager(      
													options.Messages_databaseUri,
													options.Messages_Database,
													options.Messages_Collection    )
			init_without_error = False
		except Exception as e:
			print(f'MongoDB connect error, pause for next try {next_try_delay} secons\nError {e}')
			time.sleep(next_try_delay)
except KeyboardInterrupt:
	print("Execution stopped by user (Ctrl+C)")
	exit()



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()
	active_connections.append(websocket)  # Добавляем новое подключение в список
	try:
		while True:
			data = await websocket.receive_text()
			site_request = json.loads(data)
			rich.print(site_request)
			if site_request['command'] == "GetMessagesLast":
				result = MessangerManager.get_last_messages(username=site_request.username)
				await websocket.send_json(result)
			elif site_request['command'] == "AddMessage":
				result = MessangerManager.save_message(	username=site_request['username'],
														message_text=site_request['message_text'],
														icon_name=site_request['icon'],
														hyperlink=site_request['hyperlink'])
				await websocket.send_json(result)
	except Exception as e:
		print(f"An error occurred: {e}")
	finally:
		active_connections.remove(websocket)  # Удаляем закрытое подключение из списка
		try:
			await websocket.close()  # Закрываем соединение
		except: pass

# Функция для отправки сообщения всем активным подключениям
async def send_message_to_all(message):
	for connection in active_connections:
		await connection.send_json(message)



@app.get("/restart")
async def restart_service():
    try:
        # Выполняем команды для перезапуска сервиса
        commands = [
            "cd /home/acidos/voc/memer.site/MessageLogServer",
            "source /home/acidos/voc/memer.site/MessageLogServer/venv/bin/activate",
            "python3 mainSockets.py"
        ]
        # Объединяем команды в одну строку и выполняем ее
        full_command = " && ".join(commands)
        subprocess.run(full_command, shell=True, check=True)
        return {"message": "Service restarted successfully"}
    except Exception as e:
        # Если возникла ошибка при выполнении команд, возвращаем сообщение об ошибке
        return {"error": str(e)}