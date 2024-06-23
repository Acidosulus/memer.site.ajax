from shelve import DbfilenameShelf
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
from settings import Options
from typing import Dict, Any
import datetime
import logging
import rich
import time

# from  notifier_bot import Telegram_Notifier

printer = pprint.PrettyPrinter(indent=12, width=120)
prnt = printer.pprint


base_storage_path = Path(os.path.abspath(os.curdir)).parent / 'Storage'
echo(style('Base storage path: ', fg='yellow') + style(base_storage_path, fg='bright_yellow'))

options = Options(Path(os.path.abspath(os.curdir)).parent /"options.ini")



db = FileInformationDB.VolumeDB(base_storage_path.parent)





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
	# if not('GetMessagesAfterId' in str(url) or 'GetMessagesLast' in str(url)):
	echo(	style(text = current_time + ' ', bg = 'blue', fg = 'bright_yellow')+
			 	style(text = method + ' ', bg = 'blue', fg = 'bright_red')+
			 	style(text = str(url) + ' ', bg = 'blue', fg = 'bright_green')+
			 	style(text = str(params) + ' ', bg = 'blue', fg = 'bright_white')+
				style(text = body.decode(), bg='blue', fg='bright_cyan'))
	return await call_next(request)


logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)



dblang = options.LANDDBURI
echo(style('datbase:', bg='bright_black', fg='bright_green')+style(dblang, fg='bright_green'))
dblang = LanguageDB(dblang, autocommit=False )


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


class Tile(BaseModel):
	username:str
	useruuid:str
	tile_id:int
	name:str
	hyperlink:str
	icon:str
	color:str

@app.get("/")
async def main():
	return {"message": "Hello World"}

@app.post("/Save_Tile/")
async def SaveTile(tile:Tile):
	result = dblang.SaveTile(	tile_id = tile.tile_id,
						 		user_name = tile.username,
				  				name = tile.name,
				   				hyperlink = tile.hyperlink,
								icon = tile.icon,
			 					color = tile.color)
	print(result)
	return result

@app.post("/Get_Tiles/")
async def Get_Tiles(rq:SiteRequest):
	tiles = dblang.GetTiles(rq.username)
	tiles_list = []
	sub_list = []
	for number, tile in enumerate(tiles):
		sub_list.append(tile)
		if (number+1)%6==0:
			if len(sub_list)>0:
				tiles_list.append(sub_list)
				sub_list=[]
	if len(sub_list)>0:
		tiles_list.append(sub_list)
	return JSONResponse(tiles_list)
	
@app.post("/Get_Tile/")
async def Get_Tile(rq:SiteRequest):
	return dblang.GetTile(rq.username, rq.data)


@app.post("/Delete_Tile/")
async def Delete_Tile(rq:SiteRequest):
	dblang.DeleteTiles(rq.username, rq.data)
	return 'ok'

@app.get("/Get_Rows/")
async def Get_Rows(username, useruuid:str):
	 return dblang.GetRows(username)

@app.post("/Get_Pages/")
async def Get_Pages(rq:SiteRequest):
	"""
	return list of current user pages
	"""
	return dblang.GetPages(rq.username)


@app.put("/Set_Page_As_Default/")
async def Get_Pages(rq:SiteRequest):
	"""
	set page as default\n
		data - page_id
	"""
	return dblang.SetPageAsDefault(user_name = rq.username, page_id = int(rq.data))


@app.post("/Get_Row/")
async def Get_Row(rq:SiteRequest):
	return dblang.GetHPRowData(rq.username, int(rq.data))


@app.post("/Save_Row/")
async def Save_Row(rq:SiteRequest):
	return dblang.SaveRowName(rq.username, int(rq.data), rq.comment)


@app.post("/Delete_Row/")
async def Delete_Row(rq:SiteRequest):
	return dblang.Delete_Row(rq.username, int(rq.data))


@app.delete("/Delete_Page/")
async def Delete_Page(rq:SiteRequest):
	"""
	Delete page\n
		data - page_id\n
	"""
	return dblang.Delete_Page(rq.username, int(rq.data))

@app.post("/Get_Page/")
async def Delete_Page(rq:SiteRequest):
	"""
	Get page information\n
		data - page_id\n
	"""
	return dblang.GetHPPageData(rq.username, int(rq.data))


@app.delete("/Remove_Row_From_Page/")
async def Remove_Row_From_Page(rq:SiteRequest):
	"""
	Remove row from page\n
		data - page id\n
		comment - row_id\n
	"""
	return dblang.Remove_Row_From_Page(user_name=rq.username, page_id=int(rq.data), row_id=int(rq.comment))


@app.post("/Add_Row_Into_Page/")
async def Add_Row_Into_Page(rq:SiteRequest):
	"""
	Add row into the page\n
		comment:  row_id\n
		data: page_id\n
	"""
	return dblang.AddRowIntoPage(user_name = rq.username, page_id=int(rq.data), row_id=int(rq.comment))
	



@app.post("/Move_In_Page_Row/")
async def Move_In_Page_Row(rq:SiteRequest):
	"""
	Move row up or down into the page\n
		command: direction, 'up'|'down'\n
		comment:  row_id\n
		data: page_id\n
	"""
	return dblang.Move_In_Page_Row(user_name=rq.username, direction=rq.command, page_id=int(rq.data), row_id=int(rq.comment))



@app.post("/AddTileToRowRelation/")
async def AddTileToRowRelation(rq:SiteRequest):
	dblang.AddTileToRowRelation(user_name = rq.username, row_id=int(rq.command), tile_id=int(rq.comment), index_id=int(rq.data))
	return ''

@app.post("/DeleteTileFromRow/")
async def DeleteTileFromRow(rq:SiteRequest):
	dblang.DeleteTileFromRow(rq.username, int(rq.data))
	return ''


@app.post("/GetMessagesAfterId/")
async def GetMessagesAfterId(rq:SiteRequest):
	result = dblang.GetMessagesAfterId(rq.username, int(rq.data))
	return result


@app.post("/GetMessagesLast/")
async def GetMessagesLast(rq:SiteRequest):
	result = dblang.GetMessagesLast(rq.username, int(rq.data))
	return result


@app.post("/AddMessage/")
async def AddMessage(rq:SiteRequest):
	return dblang.AddMessage(rq.username, rq.data, rq.comment, rq.command)


@app.get("/GetAllUsers/{key}/")
async def Get_All_Users(key:str):
	if key == options.SECRET_KEY:
		return JSONResponse({'status':'ok', 'users':dblang.GetUsers()})
	else:
		return JSONResponse({'status':'error, wrong secret key'})

@app.post("/get_user_information/")
async def get_user_information(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = rq.username
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_words_inprocess/")
async def get_user_count_of_words_inprocess(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetCountOfUserSyllables(rq.username, 0)
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_paragraphs_read_today/")
async def get_user_count_of_paragraphs_read_today(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetTodayReadingParagraphs(rq.username)
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_words_ready/")
async def get_user_count_of_words_ready(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetCountOfUserSyllables(rq.username, 1)
	print(response)
	return JSONResponse(response)

@app.post("/get_user_count_of_words_proceed_today/")
async def get_user_count_of_words_proceed_today(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetCountOfUserSyllablesWorkedOutToday(rq.username)
	print(response)
	return JSONResponse(response)

@app.post("/Get_Phrases_Count_Repeated_Today/")
async def Get_Phrases_Count_Repeated_Today(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetPhrasesCountRepeatedToday(rq.username)
	print(response)
	return JSONResponse(response)



@app.post("/get_last_opened_book_id/")
async def get_last_opened_book_id(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetLasReadedBookByUser(rq.username)
	print(response)
	return JSONResponse(response)



@app.post("/syllables_slices_count/")
async def syllables_slices_count(rq:SiteRequests):
	print("************************")
	print("/syllables_slices_count/")
	prnt(rq)
	response = {}
	printSiteRequests(inspect.currentframe().f_code.co_name, rq)
	response['data'] = dblang.GetCountOfSyllableSlices(rq.username, int(rq.data.split(',')[1]), int(rq.data.split(',')[0]))
	print(response)
	return JSONResponse(response)


@app.post("/get_syllable_full_data/")
async def get_syllable_full_data(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetSyllable(rq.data, rq.username) 
	for i in range(len(response['examples'])):
		response['examples'][i]['linkcode'] = base64.b64encode(bytes(response['examples'][i]['example'].replace('?', '.'), 'utf-8')).decode()
	return JSONResponse(response)


@app.post("/update_syllable_as_viewed/")
async def update_syllable_as_viewed(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.SetSylalbleAsViewed(word=rq.data, user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_Next_Syllable_For_Learning/")
async def Get_Next_Syllable_For_Learning(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetNextSyllableForLearning(user_name=rq.username)
	return JSONResponse(response)


@app.post("/Set_Syllable_Status/")
async def Set_Syllable_Status(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.SetSyllableStatus(word=rq.comment, user_name=rq.username, status=int(rq.data))
	return JSONResponse(response)


@app.post("/Get_Phrases/")
async def Get_Phrases(rq:SiteRequest):
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetPhrases(user_name=rq.username, status=int(rq.data))
	return JSONResponse(response)

@app.post("/Get_Phrase/")
async def Get_Phrase(rq:SiteRequest):
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetPhrase(user_name=rq.username, phrase_id = int(rq.data))
	response['linkcode'] = base64.b64encode(bytes(response['phrase'], 'utf-8')).decode()
	return JSONResponse(response)


@app.post("/Set_Phrase_Status/")
async def Set_Phrase_Status(rq:SiteRequest):
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.SetPhraseStatus(user_name=rq.username, status=int(rq.data), phrase_id=int(rq.comment))
	return JSONResponse(response)


@app.post("/Update_phrase_as_viewed/")
async def Update_phrase_as_viewed(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.SetPhraseAsViewed(phrase_id=int(rq.data), user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_Next_Phrase_For_Learning/")
async def Get_Next_Phrase_For_Learning(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetNextPhraseForLearning(user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_User_Books/")
async def Get_User_Books(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetUserBooks(user_name=rq.username)
	return JSONResponse(response)


@app.post("/Get_Book_Information/")
async def Get_Book_Information(rq:SiteRequest):
	response = {}
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	response = dblang.GetUserBookInformation(user_name=rq.username, id_book=int(rq.data))
	return JSONResponse(response)
	
@app.post("/Get_Paragraphs/")
async def Get_Paragraphs(rq:SiteRequest):
	response = []
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	data = rq.data.split(',') # id_book, current paragraph, how many paragraphs down to current we must return
	prnt(data)
	for i in range(int(data[2])):
		subresult = dblang.GetUserBookParagraph('admin',int(data[0]),int(data[1])+i)
		for j in range(len(subresult)):
			subresult[j]['mime'] = base64.b64encode(bytes(subresult[j]['sentence'].replace('?', '.'), 'utf-8')).decode()
		if len(subresult)>0:
			response.append(subresult)
	return JSONResponse(response)

@app.post("/Set_Book_Position/")
async def Set_Book_Position(rq:SiteRequest):
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	data = rq.data.split(',') # id_book, new_current_paragraph
	return dblang.SaveBookPosition(user_name=rq.username, id_book=int(data[0]), new_current_paragraph=int(data[1]) ) 

@app.post("/Get_List_Of_User_Syllable_From_Paragraphs_Id/")
async def Get_List_Of_User_Syllable_From_Paragraphs_Id(rq:SiteRequest):
	printSiteRequest(inspect.currentframe().f_code.co_name, rq)
	return JSONResponse({'words':dblang.GetListOfUserSyllableFromParagraphsId(rq.username, int(rq.comment), rq.data.split(','))})

def printSiteRequest(procedure, rq):
	echo(	style(text=procedure, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))

def printSiteRequests(procedure, rq):
	echo(	style(text=procedure, bg='bright_black', fg='bright_yellow') + ' ' +
			style(text='username:', bg='bright_black', fg='bright_green')+style(text=rq.username, fg='bright_green') +  ' ' +
			style(text='useruuid:', bg='bright_black', fg='bright_green')+style(text=rq.useruuid, fg='bright_green') +  ' ' +
			style(text='command:', bg='bright_black', fg='bright_green')+style(text=rq.command, fg='bright_green') + ' ' +
			style(text='comment:', bg='bright_black', fg='bright_green')+style(text=rq.comment, fg='bright_green') + ' ' +
			style(text='data:', bg='bright_black', fg='bright_green')+style(text=rq.data, fg='bright_green'))


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
async def Save_Syllabe(rq:Dict[Any, Any]):
	print("==========================================================================")
	prnt(rq)
	print("==========================================================================")
	response = {}
	prnt(rq)
	prnt(type(rq))
	syl = Syllable(	syllable_id=int(rq['syllable_id']),
					username=rq['username'],
					command=rq['command'],
					word=rq['word'],
					transcription=rq['transcription'],
					translations=rq['translations'],
					examples = rq['examples']
					)
	response = dblang.SaveSyllable(syl)
	return JSONResponse(response)

@app.post("/Save_Phrase/")
async def Save_Phrase(rq:SiteRequests):
	printSiteRequests(inspect.currentframe().f_code.co_name, rq)
	response = dblang.SavePhrase(user_name = rq.username, phrase_id=int(rq.command), text=rq.comment, translate=rq.data)
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
	

@app.post("/home_page_go_to_link_by_tile/")
async def home_page_go_to_link_by_tile(rq:SiteRequest):
	dblang.SaveTransition(user_name=rq.username, tile_id=int(rq.data), hyperlink=rq.comment)
	return ''


class RaWBook(BaseModel):
	user_name:str
	file_name:str
	book_name:str
	data:List[str]




@app.post('/add_new_book/')
async def add_new_book(rq:RaWBook):
	import asyncio
	await asyncio.get_event_loop().run_in_executor(None, dblang.Prepare_Book, rq.user_name, rq.book_name, rq.data)
	return ''