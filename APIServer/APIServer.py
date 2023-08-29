from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from typing import Union, List
from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
import FileInformationDB
from pathlib import Path
import os
from click import echo, style
from DB_Service import *
from fastapi.middleware.cors import CORSMiddleware
import configparser 
import sys
import inspect
import base64
import pprint
import json

printer = pprint.PrettyPrinter(indent=12, width=120)
prnt = printer.pprint

base_storage_path = Path(os.path.abspath(os.curdir)).parent / 'Storage'
echo(style('Base storage path: ', fg='yellow') + style(base_storage_path, fg='bright_yellow'))

config = configparser.ConfigParser()
config.read("options.ini")
SELF_ADRESS = config[sys.platform]["webserver"]
API_ADRESS = config[sys.platform]["apiserver"]
print(f'SELF_ADRESS:{SELF_ADRESS}')
print(f'API_ADRESS:{API_ADRESS}')


db = FileInformationDB.VolumeDB(base_storage_path.parent)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[SELF_ADRESS, API_ADRESS],
    allow_credentials=True, 
 	allow_methods=["*"], 
 	allow_headers=["*"]
)


#@app.middleware("http")
#async def middleware(request: Request, call_next):
#    print("middleware:","request.headers:", request.headers)
#    print("middleware:","request.body:", request.body)
#    return await call_next(request)


if sys.platform == 'linux':
	dblang = db_path =  "postgresql+psycopg2://postgres:321@185.112.225.153:35432/language"
else:
	dblang = db_path =  "postgresql+psycopg2://postgres:321@127.0.0.1:35432/language"
echo(style('datbase:', bg='bright_black', fg='bright_green')+style(db_path, fg='bright_green'))
dblang = LanguageDB(db_path, autocommit=False )


class SiteRequest(BaseModel):
	username:str
	command:str
	comment:str
	data:str

SECRETKEY='==dfffffffffffsdfe11231lklSDf234FFFFf--23====pppasdffffffffffffffffdfdfsqqwev.,.m,mzxewfffsdf=='

@app.get("/GetAllUsers/{key}/")
async def Get_All_Users(key:str):
	if key == SECRETKEY:
		return JSONResponse({'status':'ok', 'users':dblang.GetUsers()})
	else:
		return JSONResponse({'status':'error'})

@app.post("/get_user_information/")
async def get_user_information(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response['data'] = rq.username
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_words_inprocess/")
async def get_user_count_of_words_inprocess(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response['data'] = dblang.GetCountOfUserSyllables(rq.username, 0)
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_words_ready/")
async def get_user_count_of_words_ready(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response['data'] = dblang.GetCountOfUserSyllables(rq.username, 1)
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_words_proceed_today/")
async def get_user_count_of_words_proceed_today(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response['data'] = 'None'
	print(response)
	return JSONResponse(response)

@app.post("/syllables_slices_count/")
async def syllables_slices_count(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response['data'] = dblang.GetCountOfSyllableSlices(rq.username, int(rq.data.split(',')[1]), int(rq.data.split(',')[0]))
	print(response)
	return JSONResponse(response)

@app.post("/get_syllable_full_data/")
async def get_syllable_full_data(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetSyllable(rq.data, rq.username) 
	for i in range(len(response['examples'])):
		response['examples'][i]['linkcode'] = base64.b64encode(bytes(response['examples'][i]['example'].replace('?', '.'), 'utf-8')).decode()
	return JSONResponse(response)


@app.post("/update_syllable_as_viewed/")
async def update_syllable_as_viewed(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.SetSylalbleAsViewed(word=rq.data, user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_Next_Syllable_For_Learning/")
async def Get_Next_Syllable_For_Learning(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetNextSyllableForLearning(user_name=rq.username)
	return JSONResponse(response)


@app.post("/Set_Syllable_Status/")
async def Set_Syllable_Status(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.SetSyllableStatus(word=rq.comment, user_name=rq.username, status=int(rq.data))
	return JSONResponse(response)


@app.post("/Get_Phrases/")
async def Get_Phrases(rq:SiteRequest):
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetPhrases(user_name=rq.username, status=int(rq.data))
	return JSONResponse(response)

@app.post("/Get_Phrase/")
async def Get_Phrase(rq:SiteRequest):
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetPhrase(user_name=rq.username, phrase_id = int(rq.data))
	return JSONResponse(response)


@app.post("/Set_Phrase_Status/")
async def Set_Phrase_Status(rq:SiteRequest):
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.SetPhraseStatus(user_name=rq.username, status=int(rq.data), phrase_id=int(rq.comment))
	return JSONResponse(response)


@app.post("/Update_phrase_as_viewed/")
async def Update_phrase_as_viewed(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.SetPhraseAsViewed(phrase_id=int(rq.data), user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_Next_Phrase_For_Learning/")
async def Get_Next_Phrase_For_Learning(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetNextPhraseForLearning(user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_User_Books/")
async def Get_User_Books(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetUserBooks(user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_Book_Information/")
async def Get_Book_Information(rq:SiteRequest):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	response = dblang.GetUserBookInformation(user_name=rq.username, id_book=int(rq.data))
	return JSONResponse(response)
	
@app.post("/Get_Paragraphs/")
async def Get_Paragraphs(rq:SiteRequest):
	response = []
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))
	data = rq.data.split(',') # id_book, current paragraph, how many paragraphs down to current we must return
	prnt(data)
	for i in range(int(data[2])):
		subresult = dblang.GetUserBookParagraph('admin',data[0],data[1])
		if len(subresult)>0:
			response.append(subresult)
	return JSONResponse(response)


class Examples(BaseModel):
	rowid:int
	example:str
	translate:str	

class Syllable(BaseModel):
	syllable_id:int
	username:str
	command:str
	word:str
	transcription:str
	translations:str
	examples:List[Examples]

@app.post("/Save_Syllabe/")
async def Save_Syllabe(rq:Syllable):
	response = {}
	echo(	style(text=inspect.currentframe().f_code.co_name, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='syllable_id', bg='bright_black', fg='bright_green')+style(text=rq.syllable_id, fg='bright_green') + ' ' +
			style(text='word', bg='bright_black', fg='bright_green')+style(text=rq.word, fg='bright_green') + ' ' +
			style(text='transcription:', bg='bright_black', fg='bright_green')+style(text=rq.transcription, fg='bright_green') + ' ' +
			style(text='translations:', bg='bright_black', fg='bright_green')+style(text=rq.translations, fg='bright_green') + ' ' +
			style(text='examples:', bg='bright_black', fg='bright_green')+style(text=rq.examples, fg='bright_green')   )
	response = dblang.SaveSyllable(rq)
	return JSONResponse(response)



class SiteRequestWords(BaseModel):
	username:str
	ready:int
	slice_number:int
	slice_size:int
	word_part:str

@app.post('/syllables/')
async def sylalbles(rq:SiteRequestWords):
	prnt(rq)
	result = dblang.GetListOfSyllables(rq.username, int(rq.ready), int(rq.slice_size), int(rq.slice_number))
	return JSONResponse(result)

@app.post('/syllables_look_for_word_part/')
async def syllables_look_for_word_part(rq:SiteRequestWords):
	prnt(rq)
	result = dblang.GetListOfSyllablesByWordPart(user_name=rq.username, ready=int(rq.ready), slice_size=int(rq.slice_size), slice_number=int(rq.slice_number), word_part=rq.word_part)
	return JSONResponse(result)

class Media(BaseModel):
	command:str
	username:str
	folder:str
	filename:str

@app.post("/media_description/")
async def get_media(media:Media):
	if os.path.isdir(base_storage_path / media.username):
		unpackfolderpath = media.folder.replace('user_root_','').replace('|','\\').replace('\\','/').replace('//','/').replace('//','/').replace('\\\\','\\')
		userfilepath = unpackfolderpath + ('' if len(unpackfolderpath)==0 else '/') + media.filename
		userfilepath = userfilepath.replace('user_root_','').replace('|','\\').replace('\\','/').replace('//','/').replace('//','/').replace('\\\\','\\')
		filepath = os.path.join(base_storage_path , media.username, 'media',unpackfolderpath, media.filename)
		if not os.path.isfile(filepath):
			return JSONResponse({"username":media.username, "folder":media.folder, "filename":media.filename, 'status':'Error:File not found'})
		else:
			response_comment = db.GetFileText(media.username, userfilepath)
			return JSONResponse({"username":media.username, "folder":media.folder, "filename":media.filename, 'status':'Ok', 'filepath':filepath, 'userfilepath':userfilepath, 'comment':response_comment})
	else:
		 return JSONResponse({"username":media.username, "folder":media.folder, "filename":media.filename, 'status':'Error:User not found'})


class Items(BaseModel):
	username:str
	command:str
	comment:str
	folder:str
	filename:str
	
	
@app.post("/media_rename_media/")
async def media_rename_media(item:Items):
	echo(style(text=item, fg='bright_yellow', bg = 'red'))
	if os.path.isdir(base_storage_path / item.username):
		unpackfolderpath = item.folder.replace('user_root_','').replace('|','\\').replace('\\','/').replace('//','/').replace('//','/').replace('\\\\','\\')
		userfilepath = unpackfolderpath + ('' if len(unpackfolderpath)==0 else '/') + item.filename
		userfilepath = userfilepath.replace('user_root_','').replace('|','\\').replace('\\','/').replace('//','/').replace('//','/').replace('\\\\','\\')
		filepath = os.path.join(base_storage_path , item.username, 'media',unpackfolderpath, item.filename)
		print(f'filepath:{filepath}')
		echo(style(text = f'{item.comment}', fg='bright_green'))
		#print(f'decoded:{base64.b64decode(new_comment)}')
		if not os.path.isfile(filepath):
			echo(style(text=f'not os.path.isfile({filepath})', fg='bright_red'))
			return JSONResponse({'status':'Error:File not found'})
		else:
			db.UpdateInsert(user=item.username, filepath=userfilepath, comment=item.comment)
			return JSONResponse({'status':'Ok', 'userfilepath':userfilepath, 'comment':db.GetFileText(item.username, userfilepath)})
	else:
		echo(style(text=f'os.path.isdir({base_storage_path / item.username})', fg='bright_red'))
		return JSONResponse({'status':'Error:User not found'})