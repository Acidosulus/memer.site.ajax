from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from typing import Union, List
from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import os
from click import echo, style
from fastapi.middleware.cors import CORSMiddleware
import configparser 
import sys
import inspect
import base64
import pprint
import json
from settings import Options
from typing import Dict, Any
import datetime
import logging
# from  notifier_bot import Telegram_Notifier

printer = pprint.PrettyPrinter(indent=12, width=120)
prnt = printer.pprint

base_storage_path = Path(os.path.abspath(os.curdir)).parent / 'Storage'
echo(style('Base storage path: ', fg='yellow') + style(base_storage_path, fg='bright_yellow'))

options = Options("options.ini")

# tnotifier = Telegram_Notifier()
app = FastAPI()
#allow_origins=[options.SELF_ADRESS, options.API_ADRESS],

#allow_credentials=True, 
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=['*'], 
	allow_headers=["*"]
)


@app.middleware("http")
async def log_request(request: Request, call_next):
	method = request.method
	url = request.url
	params = request.query_params
	current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	body = await request.body()
	if not('GetMessagesAfterId' in str(url) or 'GetMessagesLast' in str(url)):
		echo(	style(text = current_time + ' ', bg = 'blue', fg = 'bright_yellow')+
			 	style(text = method + ' ', bg = 'blue', fg = 'bright_red')+
			 	style(text = str(url) + ' ', bg = 'blue', fg = 'bright_green')+
			 	style(text = str(params) + ' ', bg = 'blue', fg = 'bright_white')+
				style(text = body.decode(), bg='blue', fg='bright_cyan'))
	return await call_next(request)


logger = logging.getLogger("uvicorn")
#logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)



class SiteRequests(BaseModel):
	username:str
	useruuid:str
	command:str
	comment:str
	data:str

class SiteRequest(BaseModel):
	username:str
	command:str
	comment:str
	data:str


@app.get("/")
async def main():
	return {"message": "Hello World"}

