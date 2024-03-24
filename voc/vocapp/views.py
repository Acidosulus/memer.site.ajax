import base64
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django import forms
import datetime
from datetime import date, timedelta
import load_syllable_from_wooordhunt
import os.path
import os
import json
import shutil
from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponse
from gtts import gTTS
from django.contrib.auth import authenticate, login, logout
from my_library import *
from FileInformation import FileInformation
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt  
import configparser
import django.http.request
import sys
from django.conf import settings
from click import echo, style
from colorama import Fore, Back, Style
import requests
import pprint
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from UsersDataStorage import UsersDataStorage

printer = pprint.PrettyPrinter(indent=12, width=160)
prnt = printer.pprint

## users data storage with names and guids for substitutuion in html renders
echo(style(text='Get data from APIServer:', fg='yellow') + style(text=f"{settings.API_ADRESS}/GetAllUsers/{settings.SECRET_KEY}/", fg='bright_yellow'))
response = requests.get(f"{settings.API_ADRESS}/GetAllUsers/{settings.SECRET_KEY}/")
usersDataStorage = UsersDataStorage(response.content.decode('utf-8'))


# 'onchange':"document.getElementById('id_link_on_wooordhunt').href='https://wooordhunt.ru/word/'+escape(this.value)"
class UserForm(forms.Form):
	word = forms.CharField( label="Слово", widget=forms.TextInput(attrs={'class' : 'my_class_input_word'}))
	transcription = forms.CharField(label="Транскрипция", widget=forms.TextInput(attrs={'class' : 'my_class_input_transcription'} ))
	translations = forms.CharField(label="Перевод", widget=forms.Textarea(attrs={'class' : 'my_class_input_translations','rows':"7"} ))
	examples = forms.CharField(label="Примеры", widget=forms.Textarea(attrs={'class':"my_class_input_examples",'rows':"7"} ))


def load_word_to_words_db(pc_word:str):
	words_data = Words.objects.filter(word= pc_word)
	if words_data.count()==0:
			lc_link = r'https://wooordhunt.ru/word/' + pc_word
			print(lc_link)
			lo_wh = load_syllable_from_wooordhunt.Wooordhunt(lc_link)
			lc_word = pc_word
			lc_transcription = lo_wh.get_transcription()
			lc_translations = lo_wh.get_translation()
			lc_examples = lo_wh.get_examples()
			lc_parent_word = lo_wh.get_parent_word()
			print('lc_word == >', lc_word)
			print('lc_transcription == >', lc_transcription)
			print('lc_translations == >', lc_translations)
			print('lc_examples == >', lc_examples)
			print('lc_parent_word == >', lc_parent_word)
			if len(lc_transcription) != 0:
				word_to_save = Words(word = lc_word, transcription = lc_transcription, translations = lc_translations, \
									examples = lc_examples, dt = datetime.datetime.now(), notfound=0, parent_word = lc_parent_word)
				word_to_save.save()
				print('Saved - ', pc_word)
				if len(lc_transcription) == 0 and len(lc_parent_word) > 0:
					load_word_to_words_db(lc_parent_word)
			else:
				word_to_save = Words(word = lc_word, dt = datetime.datetime.now(), notfound = 1, parent_word = lc_parent_word)
				word_to_save.save()
				print('Not found - ', pc_word)
			

def load_word_to_words_db_by_book(pc_book_id:str):
	all_words = Get_list_of_words_from_book(pc_book_id)
	ln_count = len(all_words)
	ll_counter = 0
	for word in all_words:
		ll_counter += 1
		print(ll_counter, '/', ln_count, '   ', word)
		load_word_to_words_db(word)

 



def get_user_storage_path(request):
	return settings.BASE_DIR.parent / 'Storage' / request.user.username

def get_user_media_path(request):
	return  get_user_storage_path(request) / "media"

def get_user_assets_path(request):
	return  get_user_storage_path(request) / "assets"

def get_user_icons_path(request):
	return  get_user_assets_path(request) / "tiles"


def Create_User_Storage(request):
	print("User account path:", get_user_storage_path(request))
	if not os.path.exists(get_user_storage_path(request)):
		os.makedirs(get_user_storage_path(request))
	if not os.path.exists(get_user_media_path(request)):
		os.makedirs(get_user_media_path(request))
	if not os.path.exists(get_user_assets_path(request)):
		os.makedirs(get_user_assets_path(request))
	if not os.path.exists(get_user_icons_path(request)):
		os.makedirs(get_user_icons_path(request))

 

def PageLogIn(request):
	print("<<<"+">>>>")
	print(request)
	print('1------------', request.POST)
	if 'username' in request.POST and 'password' in request.POST:
		print('2-----------', request.POST['username'],request.POST['password'])
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:	
				login(request, user)
				print('3------Redirect to a success page.', user)
				Create_User_Storage(request)
				return redirect(index)
			else:
				print("4------Return a 'disabled account' error message")
		else:
			print("5-------Return an 'invalid login' error message.")		
	return render(request, "login.html")


def log_out(request):
	print(" ============== logout")
	logout(request)
	return redirect(index)


def hoster(request):
	lc_start_path = Path(__file__).resolve().parent.parent.parent / 'static'  
	print(lc_start_path)
	# lc_start_path = r'C:\voc\memer.site\voc\vocapp\static'
	catalogs = os.listdir(lc_start_path)
	catalogs.remove('css')
	catalogs.remove('images')
	catalogs.remove('js')
	catalogs.remove('sounds')
	catalogs.remove('admin')
	data={'catalogs':catalogs}
	return render(request, "hoster.html", context=data)




@csrf_exempt
def hoster_control(request,sitename:str):
	#lc_start_path = r'C:\voc\memer.site\voc\vocapp\static' + "\\" + sitename
	output = []
	total_size = 0
	lc_start_path = Path(__file__).resolve().parent.parent.parent / 'static' / sitename 
	if request.method == 'POST' and request.FILES['myFile']:
		myfile = request.FILES['myFile']
		print(myfile.name)
		print(myfile)
		from django.core.files.storage import FileSystemStorage
		fs = FileSystemStorage()
		filename = fs.save(os.path.join(lc_start_path, myfile.name), myfile)
		uploaded_file_url = fs.url(filename)
		print(uploaded_file_url)
	else:
		files = [f for f in os.listdir(lc_start_path) if os.path.isfile(os.path.join(lc_start_path, f))]
		for file in files:
			file_size = os.path.getsize(Path(__file__).resolve().parent.parent.parent / 'static' /sitename /file)
			total_size = total_size + file_size
			fl = oFile(file, file_size)
			output.append(fl)
	fl = oFile('',total_size)
	data={'sitename':sitename, 'files':output, 'files_count':len(files), 'total_size':fl.size}
	return render(request, "hoster_control.html", context=data)

def hoster_control_clear_all(request,sitename:str):
	#lc_start_path = r'C:\voc\memer.site\voc\vocapp\static' + "\\" + sitename
	lc_start_path = Path(__file__).resolve().parent.parent.parent / 'static' / sitename 
	files = [f for f in os.listdir(lc_start_path) if os.path.isfile(os.path.join(lc_start_path, f))]
	for file in files:
		os.remove(os.path.join(lc_start_path ,file))
	return redirect(hoster_control,sitename)

@login_required
def index(request):
	print(f'request.user.get_username():{request.user.get_username()}')
	print(type(usersDataStorage.data))
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], 'ready':0 }
	return render(request, "index.html", context=data)

@login_required
def ready_list(request):
	print(" ============== ready_list")
	data = {'APIServer':settings.API_ADRESS, 'ready':1, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'] }
	print(data)
	return render(request, "ready_list.html", context=data)

@login_required
def proceed_list(request):
	print(" ============== ready_list")
	data = {'APIServer':settings.API_ADRESS, 'ready':0, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'] }
	print(data)
	return render(request, "ready_list.html", context=data)



def personal_page(request):
	print(" ============== personal_page")
	data = {}
	return render(request, "personal_page.html", context=data)


def Get_list_of_words_from_book(pn_book_id:int):
	strings = Paragraphs.objects.values('paragraph').filter(id_book = pn_book_id)
	ll_all_words = []
	for string in strings.iterator():
		words = string['paragraph'].split()
		for word in words:
			clear_word = delete_non_english_alphabet_characters(word.lower().strip())
			if len(clear_word)>2 and not(clear_word in ll_all_words):
				ll_all_words.append(clear_word)
	print(len(ll_all_words))
	return ll_all_words



def rest_response(request,pc_first:str, pc_second:str, pc_third:str):
	data = { }
	print('=========', request.method)
	if request.method == 'GET':
		if pc_first == 'words':
			print(pc_second, pc_third)
		if pc_first == 'books':
			print('=========', pc_first)
			if pc_second == 'allparagraphs':
				if int(pc_third)>0:
					strings = Paragraphs.objects.values('paragraph').filter(id_book = int(pc_third), userid=request.user.id)
					data = {'paragraphs':list(strings)}
			if pc_second == 'allwords':
				#/restapi/v1/books/allwords/3/
				print('=========', pc_second)
				if int(pc_third)>0:
					#load_word_to_words_db_by_book('4')
					print('=========', pc_third)
					ll_all_words = Get_list_of_words_from_book(int(pc_third))
					data = {'words':ll_all_words}
	return JsonResponse(data)


def json_response(request, pc_type, pc_book_id):
	
	if pc_type == 'test':
		ln = Words.objects.get(word = 'pluck').rowid
		print(type(ln))
		print(ln)
		data = {'test':ln}

	if pc_type == 'word_hint':
		#####################################################################################################################################################
		word = Words.objects.get(rowid = int(pc_book_id.replace('hint','')))
		lc = ''
		sententces = word.translations.split('\r')
		for sentence in sententces:
			lc = lc +"""<p style='color:Khaki;font-size:120%;line-height:70%'>""" + sentence+ '</p>'
		data = {'word':word.word, 'transcription':word.transcription, 'translations':add_format_for_russian(lc, 'my_class_p_my_class_p_hint_translations_russian').replace(chr(13),'<br>')}
		return render(request, "hint_response.html", context=data)
	
	if pc_type == 'look_for_word':
		pc_book_id = pc_book_id.strip()
		syllable = Syllable.objects.filter(word__contains = ""+pc_book_id+"", userid=request.user.id)
		data = {'words':syllable}
		return render(request, "finding_index.html", context=data)

	if pc_type == 'book_position':
		if int(pc_book_id)>0:
			pc_paragraph = Books.objects.filter(id_book = int(pc_book_id), userid=request.user.id)[0].current_paragraph
			lo_paragraph_navigation = Paragraphs.objects.filter(id_book=int(pc_book_id), userid=request.user.id).order_by('id_paragraph')[0]
			ln_start_id = lo_paragraph_navigation.id_paragraph
			lo_paragraph_navigation = Paragraphs.objects.filter(id_book=int(pc_book_id), userid=request.user.id).latest('id_paragraph')
			ln_end_id = lo_paragraph_navigation.id_paragraph
			lc_in_book_position = str(int(pc_paragraph) - ln_start_id) + ' / ' + str(ln_end_id - ln_start_id) + ' &nbsp;&nbsp;&nbsp;' + str(round((int(pc_paragraph) - ln_start_id) * 100 / (ln_end_id - ln_start_id), 2)) + ' %'
			data = {'book_position':lc_in_book_position}

	if pc_type == 'book_name':
		if int(pc_book_id)>0:
			lc_book_name = Books.objects.filter(id_book = int(pc_book_id), userid=request.user.id)[0].book_name
			data = {'book_name':lc_book_name}

	if pc_type == 'span_number_of_words_to_study':
		data = {'span_number_of_words_to_study':str(len(Syllable.objects.filter(ready=0, userid=request.user.id).order_by('last_view')))}

	if pc_type == 'link_last_added_word':
		data = {'link_last_added_word':Syllable.objects.filter(ready=0, userid=request.user.id).filter(show_count=0).order_by('-last_view')[0].word}

	if pc_type == 'number_of_words_learned':
		data = {'number_of_words_learned':str(len(Syllable.objects.filter(ready=1, userid=request.user.id)))}
	
	if pc_type == 'user_view':
		data = {'user_view':str(request.user)}

	if pc_type == 'span_number_of_words_study_today': # количество проработанных за сегодня слов
		dataset = Syllable.objects.filter(userid=request.user.id, last_view__year=date.today().year, last_view__month=date.today().month, last_view__day=date.today().day).exclude(show_count=0)
		data = {'span_number_of_words_study_today':len(dataset)}

	return JsonResponse(data)

def test(request):
	print(" ============== test")
	pc_file_path = r'F:\voc\memer.site\voc\tg4.txt'
	lc_book_name = 'Temple Of The Winds - by Terry Goodkind'
	ll_book = open(pc_file_path, "r", encoding='utf8').readlines()
	lc_result = ''
	for lc_paragraph in ll_book:
		lc_result = lc_result + lc_paragraph.replace(chr(13), '').replace(chr(10), '').replace(chr(12), '')+chr(13)
	lc_result = lc_result.replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13))
	ll_paragraps = lc_result.split(chr(13))

	book = Books(book_name = lc_book_name, current_paragraph = 1, userid=request.user.id)
	book.save()

	for counter, lc_p in enumerate(ll_paragraps):
		print(f'{counter}/{len(ll_paragraps)}')
		print(lc_p)
		if len(lc_p):
			paragraph = Paragraphs(id_book = book.id_book, paragraph = lc_p, userid=request.user.id)
			paragraph.save()

	data = {"text":lc_result}
	return render(request, "test.html", context=data)

@login_required
def add_new_with_parameter(request, pc_new_word):
	return add_new( request, 	pc_new_word)

@login_required
def add_new(request, pc_new_word=''):
	data = {'word':pc_new_word.strip(), 'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid']}
	return render(request, "add_new_word.html", context=data)


def add_format_for_russian(pc_source:str, lc_style_name): #возвращает строку, где русские символы переданной строки отмечены указанным стилем
	lc_russian = 'йцукенгшщзхъфывапролджэячсмитьбюё'
	lc_russian = lc_russian+lc_russian.upper()
	lc_result = ''
	for lc_chr in pc_source:
		if lc_chr in lc_russian:
			lc_result = lc_result + '<span class = "' + lc_style_name+'">' + lc_chr + '</span>'
		else:
			lc_result = lc_result + lc_chr
	
	lc_result = lc_result  .replace(r'''</span><span class = "'''+lc_style_name+'''">''',   r''  ).\
							replace(r'''</span> <span class = "'''+lc_style_name+'''">''',  r' ' ).\
							replace(r'''</span>/ <span class = "'''+lc_style_name+'''">''', r'/ ').\
							replace(r'''</span> /<span class = "'''+lc_style_name+'''">''', r' /').\
							replace(r'''</span>; <span class = "'''+lc_style_name+'''">''', r'; ').\
							replace(r'''</span>, <span class = "'''+lc_style_name+'''">''', r', ').\
							replace(r'''</span>(<span class = "'''+lc_style_name+'''">''',  r'(' ).\
							replace(r'''</span>)<span class = "'''+lc_style_name+'''">''',  r')' ).\
							replace(r'''</span>( <span class = "'''+lc_style_name+'''">''', r'( ').\
							replace(r'''</span>) <span class = "'''+lc_style_name+'''">''', r') ').\
							replace(r'''</span> (<span class = "'''+lc_style_name+'''">''', r' (').\
							replace(r'''</span> )<span class = "'''+lc_style_name+'''">''', r' )').\
							replace(r'''</span>- <span class = "'''+lc_style_name+'''">''', r'- ').\
							replace(r'''</span> -<span class = "'''+lc_style_name+'''">''', r' -').\
							replace(r'''</span>-<span class = "'''+lc_style_name+'''">''',  r'-' ).\
							replace(r'''</span>. <span class = "'''+lc_style_name+'''">''', r'. ')
	print(lc_result)
	return lc_result


def DownLoadExamples(pl_list):
	for part in pl_list:
		lc_example = part.split('\n')
		if len(lc_example[0])>10:
			lc_file_name = load_syllable_from_wooordhunt.Delete_from_String_all_Characters_Unsuitable_For_FileName(lc_example[0])
			lc_full_file_name = Path(__file__).resolve().parent.parent / 'static' / 'sounds' / 'examples' /  lc_file_name / '.mp3'
			if not os.path.exists(lc_full_file_name):
				try:
					ts = gTTS(lc_example[0], lang='en')
					ts.save(lc_full_file_name)
					print('saved:', lc_example[0], 'file:', lc_full_file_name)
				except:
					pass
	return lc_full_file_name

@login_required
def word_in_progress(request, pc_word=''):
	print(f"wordinprogress	 pc_word:{pc_word}")
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], 'word':pc_word.strip()}
	return render(request, "word_in_progress.html", context=data)


def DownLoadmp3s (sentence):
	lc_file_name = sentence + '.mp3'
	lc_full_file_name = Path(__file__).resolve().parent.parent.parent / 'static' / 'sounds' / 'books' / lc_file_name
	lc_sentence = base64.b64decode(sentence).decode()
	if not (os.path.exists(str(lc_full_file_name))) and len(lc_sentence) > 4:
		try:
			ts = gTTS(lc_sentence, lang='en')
			ts.save(str(lc_full_file_name))
			print('saved:', lc_sentence, 'file:', str(lc_full_file_name))
		except:
			pass
	return str(lc_full_file_name)


@login_required
def books(request):
	#lo_book = Books.objects.filter(userid=request.user.id).order_by('-dt')
	#data = { 'books':lo_book }
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], 'body_id':'id_body_books'}
	return render(request, "books.html", context=data)

@login_required
def book(request, pc_book:str):
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], "id_book":pc_book}
	return render(request, "book.html", context=data)

def read_last_opened_book(request):

	curl = f"{settings.API_ADRESS}/get_last_opened_book_id/"
	r = requests.post(curl, json.dumps({"username":request.user.username, "command":"", "comment":"", "data":""}))
	echo(style(text='cross_request => ', fg='yellow')+' '+
		style(text=curl, fg='yellow'))
	print(Fore.LIGHTGREEN_EX,end='')
	prnt(r.text)
	print(Fore.RESET,end='')
	print('-------------------------cross_request------------------------', datetime.datetime.now())
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], "id_book":json.loads(r.text)['data']}
	return render(request, "book.html", context=data)

def get_sentence(request, pc_sentence:str):
	lc_file_name = DownLoadmp3s(pc_sentence)
	fsock = open(lc_file_name, 'rb')
	response = HttpResponse(fsock, content_type='audio/mpeg')
	response['Content-Type'] = 'audio/mp3'
	response['Content-Disposition'] = "attachment; filename=%s" % \
			(lc_file_name.replace(' ', '-'), )
	response['Content-Length'] = \
		os.path.getsize(lc_file_name)
	return response

@login_required
def next_with_last(request, pc_last_word):
	print(" ============== next_with_last")
	lo_sillable = Syllable.objects.get(word = pc_last_word, userid=request.user.id)
	lo_sillable.show_count = lo_sillable.show_count + 1
	lo_sillable.last_view = datetime.datetime.now()
	lo_sillable.save()
	return redirect(next)

@login_required
def ready(request, pc_ready_word):
	print(" ============== ready")
	lo_sillable = Syllable.objects.get(word = pc_ready_word, userid=request.user.id)
	lo_sillable.ready = 1
	lo_sillable.save()
	print('===================')
	print("ready:",pc_ready_word)
	print('===================')
	return redirect(index)

@login_required
def unready(request, pc_unready_word):
	lo_sillable = Syllable.objects.get(word = pc_unready_word, userid=request.user.id)
	lo_sillable.ready = 0
	lo_sillable.save()
	print('===================')
	print("unready:",pc_unready_word)
	print('===================')
	return redirect(ready_list)

@login_required
def phrases(request):
	data = { 'readystatus':0, 'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'] }
	return render(request, "phrases.html", context=data)

@login_required
def phrases_ready_list(request):
	data = { 'readystatus':1 , 'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'] }
	return render(request, "phrases.html", context=data)


@login_required
def phrases_add_new(request, pc_phrase_id):
	data = { "modify_type":'new', "phrase_text":'', "phrase_translation":'', "phrase_id":pc_phrase_id,
			 'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid']}
	return render(request, "phrases_modify.html", context=data)


@login_required
def phrases_in_progress_with_id(request, pc_phrase_id):
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], 'phrase_id':pc_phrase_id}
	return render(request, "phrase_in_progress.html", context=data)

@login_required
def phrases_in_progress(request):
	data = {'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'], 'phrase_id':0}
	return render(request, "phrase_in_progress.html", context=data)


# список каталогов, находящихся по переданному пути, без вложенности
def Get_Catalogs_List(path:str) -> list:
	print(f'os.listdir(path):{path}')
	content = os.listdir(path)
	catalogs = []
	for catalog in content:
		if os.path.isdir(os.path.join(path, catalog)):
			catalogs.append(catalog)
	return catalogs

# список картинок, находящихс по переданному пути
def Get_Images_List(path:str) -> list:
	print(f"Get_Images_List path: {path}")
	content = os.listdir(path)
	images = []
	for file in content:
		if os.path.isfile(os.path.join(path, file)) and (file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png') or file.endswith('.PNG') or file.endswith('.JPEG')  or file.endswith('.jpeg')):
			images.append(file)
	return images

def media_list_02(request, folder_01:str, folder_02:str):
	return media_list(request, folder_01 + "/" + folder_02)


# список каталогов каталого media залогиненного пользователя
@login_required
def media_list(request, folder_01:str):
	echo(	style(text="=================== media_list(request, '", fg="bright_yellow")+
	  		style(text=f"{folder_01}", fg='bright_green')+
			style(text="') =================", fg="bright_yellow") )
	folder_01 = folder_01.replace("|", "/")
	print(f"{Fore.LIGHTYELLOW_EX}media_list -> folder_01: {Fore.LIGHTGREEN_EX}{folder_01}{Fore.RESET}")
	if folder_01.upper() == "user_root_".upper():
		lc_dir = get_user_media_path(request) # root user media folder
	else:
		print(f"+{folder_01}")
		lc_dir = get_user_media_path(request) / folder_01
	print(f"lc_dir:{lc_dir}")
	# user media directories
	directory_names_list = Get_Catalogs_List(lc_dir)
	directories_list = []
	for dir in directory_names_list:
		row = {	'dir_name':dir,
	 			'link':"/media_list/"+(dir if folder_01.upper() == "user_root_".upper() else f"{folder_01}/{dir}/").replace("/","|").replace("||","|"),
				'delete_link':(dir if folder_01.upper() == "user_root_".upper() else f"{folder_01}/{dir}/").replace("/","|").replace("||","|"),
				'rename_link':(dir if folder_01.upper() == "user_root_".upper() else f"{folder_01}/{dir}/").replace("/","|").replace("||","|")
				}
		directories_list.append(row)
	# user media in current directory
	ml = Get_Images_List(lc_dir)
	media_list=[]
	for media in ml:
		lc_media_link = ("/api/v1/get_media_source/"+folder_01.replace("/",'|') +"/"+ media).replace("||","|")
		lc_delete_link = (media if folder_01.upper() == "user_root_".upper() else f"{folder_01}/{media}").replace("/","|").replace("||","|")
		lc_rename_link = media #(media if folder_01.upper() == "user_root_".upper() else f"{folder_01}/{media}").replace("/","|")
		print(	f'----------{Fore.YELLOW}media:{Fore.LIGHTGREEN_EX}{media}------------\n'+
				f'{Fore.YELLOW}lc_media_link:{Fore.LIGHTGREEN_EX}{lc_media_link}\n'+
				f'{Fore.YELLOW}lc_delete_link:{Fore.LIGHTGREEN_EX}{lc_delete_link}\n'+
				f'{Fore.YELLOW}lc_rename_link:{Fore.LIGHTGREEN_EX}{lc_rename_link}')
		media_list.append({	'media_link':lc_media_link,
			 				'delete_link':lc_delete_link,
			 				'rename_link':lc_rename_link,
							'file_name':media })
	#		'rename_link':(media if folder_01.upper() == "user_root_".upper() else f"{folder_01}/{media}").replace("/","|")}
	current_folder_name = folder_01.replace('/','|')
	print(f'{Fore.LIGHTYELLOW_EX}current_folder_name:{Fore.LIGHTBLUE_EX}{current_folder_name}')
	data = {
			'directories':directories_list,
			'medias':media_list,
			'current_folder_name':current_folder_name,
			'user_name':request.user.username}
	print()
	print(data)
	print(Fore.RESET)
	return render(request, "media_list.html", context=data)




@csrf_exempt
def cross_request(request):
	print('-------------------------cross_request------------------------', datetime.datetime.now())
	req = request.body.decode('utf-8').replace('"username":""',f'"username":"{request.user.username}"')
	print('----------------------- raw body ------------------')
	prnt(req)
	print('---------------------------------------------------')
	jdata = json.loads(req)
	print(Fore.LIGHTCYAN_EX,end='')
	prnt(jdata)
	print(Fore.RESET,end='')
	curl = f"{settings.API_ADRESS}/{jdata['command']}/"
	r = requests.post(curl, req.encode())
	echo(style(text='cross_request => ', fg='yellow')+' '+
		style(text=curl, fg='yellow'))
	print(Fore.LIGHTGREEN_EX,end='')
	prnt(r.text)
	print(Fore.RESET,end='')
	print('-------------------------cross_request------------------------', datetime.datetime.now())
	return HttpResponse(r.text)



@csrf_exempt
def cross_request_no_response(request):
	curl = f'{settings.API_ADRESS}/cross_request/'
	print()
	print('-------------------------cross_request------------------------')
	req = request.body.decode('utf-8').replace('"username":""',f'"username":"{request.user.username}"')
	print(req)
	print()
	r = requests.post(curl, req.encode())
	echo(style(text='cross_request => ', fg='yellow')+' '+
		style(text=curl, fg='yellow')+' '+
	  	style(text=r.text, fg='green'))
	return HttpResponse(r.text)

@csrf_exempt
def media_cross_request_get(request):
	curl = f'{settings.API_ADRESS}/media_description/'
	r = requests.post(curl, request.body)
	response = sx(r.text, '"comment":"', '"')
	echo(style(text='media_cross_request_get => ', fg='yellow')+' '+
		style(text=curl, fg='yellow')+' '+
	  	style(text=response, fg='green'))
	return HttpResponse(response)


@csrf_exempt
def media_edit_comment(request:django.http.request.HttpRequest):
	echo(style(text = f"=====================>media_edit_comment", fg = 'bright_red'))
	curl = f'{settings.API_ADRESS}/media_rename_media/'
	echo("curl:"+style(text={curl},fg='bright_magenta')+" body:"+style(text = request.body, fg = 'bright_red'))
	print(f'====================================={request.user.username}======================')
	rbody = request.body
	echo(style('body:', fg='yellow')+style(text = rbody, fg='bright_yellow'))
	r = requests.post(curl, data=rbody)
	response = sx(r.text, '"comment":"', '"')
	echo(style(text=curl, fg='blue')+' '+
	  	style(text=response, fg='green'))
	return HttpResponse(response)


def get_user_media(request, folder:str, file:str):
	folder = folder.replace("|","/")
	lc_path = get_user_media_path(request) / ( folder.replace("|","/") if folder.upper()!="USER_ROOT_" else "") / file
	print(f'Sent media:{lc_path}')
	with open(lc_path, mode='br') as fh:
		return HttpResponse(fh.read(), content_type='content/image')
	
def example(request, ):
	data = {}
	return render(request, "example.html", context=data)

def dragTest(request, ):
	data = {}
	return render(request, "dragTest.html", context=data)

@csrf_exempt
@login_required
def Upload_User_Media(request:django.http.request.HttpRequest, user_folder:str):
	print("=========================Upload_User_Media============================")
	lc_path = get_user_media_path(request) / ( user_folder.replace("|","/") if user_folder.upper()!="USER_ROOT_" else "")
	print(f'user_folder:{user_folder}')
	print(f'lc_path:{lc_path}')
	print('request.content_params   ', request.content_params)	
	print('request.FILES   ',   request.FILES)
	print('request.content_type   ',   request.content_type)
	print('request.FILES.keys()   ', request.FILES.keys())
	print('request.FILES.getlist()   ', request.FILES.getlist('files'))
	print('==>')
	#lc_error_text = ''
	for file in request.FILES.getlist('files'):
		#name = file.name
		content = file.read()
		print(f'FileName: {file.name} Content Type: {file.content_type} FileSize: {file.size} ContentPythonType: {type(content)}, Content: {content}')
		with open(Get_Uniqie_file_name(lc_path / file.name), "wb") as binary_file:
			binary_file.write(content)
	return redirect(f'/media_list/{user_folder}/')

# в случае если файл с заданным именем уже существует возвращает путь к новому файлу по типу (файл номер расширвание)
def Get_Uniqie_file_name(pc_file_name:str) -> str:
	if os.path.exists(pc_file_name):
		counter = 0
		filename, file_extension = os.path.splitext(pc_file_name)
		filename = filename+"{}"+file_extension
		while os.path.isfile(filename.format(counter)):
			counter += 1
			filename = filename.format(counter)
			return filename
	else:
		return pc_file_name

@login_required
def create_user_media_folder(request:django.http.request.HttpRequest, folder:str, created_volume:str):
	print(f'get_user_media_path: {get_user_media_path(request)}')
	print(f'folder: {folder}')
	print(f'created_volume: {created_volume}')
	print(f'get_user_storage_path(request):{get_user_storage_path(request)}')
	lc_path = get_user_media_path(request) / folder.replace("|","/") / created_volume
	try:
		#print(f'{folder.upper()}!="USER_ROOT_": ', folder.upper()!="USER_ROOT_")
		#print(type(folder.upper()))
		#print(type("USER_ROOT_"))
		lc_in_dir = get_user_media_path(request) / ( folder.replace("|","/") if folder.upper()!="USER_ROOT_" else "")
		print(f'lc_in_dir:{lc_in_dir}')
		#print(f'os.path.isdir(lc_path):{os.path.isdir(lc_path)}')
		os.chdir(lc_in_dir)
		os.mkdir(created_volume)
	except Exception as e:return HttpResponse(f'get_user_media_path: {get_user_media_path(request)}\nfolder: {folder}\ncreated_volume: {created_volume}\nlc_path: {lc_path}\n\n' + 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'\n\n' + type(e).__name__ +'\n\n' + e.__str__())
	else:	return HttpResponse('success')
	
@login_required
def delete_user_media_folder(request:django.http.request.HttpRequest, folder:str):
	print(f'folder: {folder}')
	try:
		lc_in_dir = get_user_media_path(request) / ( folder.replace("|","/") if folder.upper()!="USER_ROOT_" else "")
		print(f'deleted folder: {lc_in_dir}')
		if os.path.isdir(lc_in_dir):
			if str(get_user_media_path(request)) in str(lc_in_dir):
				shutil.rmtree(lc_in_dir)
		if os.path.isfile(lc_in_dir):
			os.remove(lc_in_dir)
	except Exception as e:	return HttpResponse(f'get_user_media_path: {get_user_media_path(request)}\nfolder: {folder}\ndeleted folder: {folder}\nlc_in_dir: {lc_in_dir}\n\n' + 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'\n\n' + type(e).__name__ +'\n\n' + e.__str__())
	else:	return HttpResponse('success')

@login_required
def rename_user_media_folder(request:django.http.request.HttpRequest, current_folder:str, last_folder_name:str, new_folder_name:str):
	lc_in_dir = get_user_media_path(request) / ( current_folder.replace("|","/") if current_folder.upper()!="USER_ROOT_" else "")
	echo(	style(text=f'current_folder:', fg='bright_yellow')+
			style(text=f'{current_folder}', fg='bright_green')+
			'	'+
			style(text=f'last_folder_name:', fg='bright_yellow')+
			style(text=f'{last_folder_name}', fg='bright_green')+
			'	'+
			style(text=f'new_folder_name:', fg='bright_yellow')+
			style(text=f'{new_folder_name}', fg='bright_green')+
			'	'+
			style(text=f'lc_in_dir:', fg='bright_yellow')+
			style(text=f'{lc_in_dir}', fg='bright_green')
			)
	try:
		print(f'{Fore.YELLOW}get_user_media_path(request):{Fore.LIGHTWHITE_EX}{get_user_media_path(request)}{Fore.RESET}')
		src = get_user_media_path(request) / ( current_folder.replace("|","/") if current_folder.upper()!="USER_ROOT_" else "") / last_folder_name
		if os.path.isfile(src):
			dest = (get_user_media_path(request) / ( current_folder.replace("|","/") if current_folder.upper()!="USER_ROOT_" else "")) / new_folder_name.replace("|","/")
		else:
			dest = (get_user_media_path(request) / ( current_folder.replace("|","/") if current_folder.upper()!="USER_ROOT_" else "")) / new_folder_name
		echo(	style(text=f'src:', fg='bright_yellow')+
	 		style(text=f'{src}', fg='bright_green')+
			'	'+
			style(text=f'dest:', fg='bright_yellow')+
			style(text=f'{dest}', fg='bright_green')
			)
		os.rename(src, dest)
	except Exception as e:	return HttpResponse(f'get_user_media_path: {get_user_media_path(request)}\ncurrent_folder: {current_folder}\nlast_folder_name: {last_folder_name}\nnew_folder_name:{new_folder_name}\nlc_in_dir: {lc_in_dir}\n\n' + 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'\n\n' + type(e).__name__ +'\n\n' + e.__str__())
	else:	return HttpResponse('success')


def GetWoorhuntDataJSON(request, pc_word:str):
	result = {}
	if len(pc_word)>0:
		lo_wh = load_syllable_from_wooordhunt.Wooordhunt(r'https://wooordhunt.ru/word/' + pc_word)
		result['word'], result['transcription'], result['translations'], result['examples'] = pc_word, lo_wh.get_transcription(), lo_wh.get_translation(), GetDividedExamplesWH(lo_wh.get_examples())
		#prnt(result)
	return JsonResponse(result)


def GetDividedExamplesWH(source:str):
	result = []
	for part in source.split('\n\n'):
		ll_example = part.split('\n')
		
		try:str_example = ll_example[0]
		except:str_example = ''

		try:str_translate = ll_example[1]
		except:str_translate = ''
		if len(str_example)>0:
			result.append({'example':str_example, 'translate':str_translate})
	return result


 
@login_required
def edit_tile(request, tile_id=''):
	data = {	'APIServer':settings.API_ADRESS,
         		'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid'],
           		'tile_id':tile_id}
	print(style(text=data, fg='bright_yellow'))
	return render(request, "./home_page/edit_tile.html", context=data)



def find_files_by_extension(folder_path, extensions):
	if not os.path.isdir(folder_path):
		print(f"Ошибка: {folder_path} не является папкой.")
		return []
	files_with_dates = []
	for root, dirs, files in os.walk(folder_path):
		for file in files:
			if os.path.splitext(file)[1].upper() in extensions:
				file_path = os.path.join(root, file)
				creation_time = os.path.getctime(file_path)
				files_with_dates.append((file_path, creation_time))
	sorted_files = sorted(files_with_dates, key=lambda x: x[1])
	return [os.path.basename(file[0]) for file in sorted_files]


@login_required
def get_user_asset(request, folder:str, file:str):
	folder = folder.replace("|","/")
	lc_path = get_user_assets_path(request) / ( folder.replace("|","/") if folder.upper()!="USER_ROOT_" else "") / file
	print(f'Sent media:{lc_path}')
	with open(lc_path, mode='br') as fh:
		response = HttpResponse(fh.read(), content_type='content/image')
	response['Cache-Control'] = 'max-age=3600*24*7'
	response['Expires'] = 'Sun, 17 Mar 2084 12:00:00 GMT'
	return response


def get_icons_lists(request):
	icons_list = []
	sub_list = []
	icons_list_source = find_files_by_extension(get_user_icons_path(request), ['.JPEG','.JPG','.GIF','.BMP','.PNG','.WEBP','.ICO','.SVG'])
	for number, icon in enumerate(icons_list_source):
		sub_list.append({'icon':icon, 'number':(((number+1)%12)+1)})
		if (number+1)%12==0:
			if len(sub_list)>0:
				icons_list.append(sub_list)
				sub_list=[]
	if len(sub_list)>0:
		icons_list.append(sub_list)
	return icons_list

@login_required
def Get_files_lists_json(request):
    result = json.dumps(get_icons_lists(request))
    return HttpResponse(result)

@login_required
def select_icon(request):
	pc_tile_id=''
	data = {'tile_id':pc_tile_id.strip(),
		 	'user_asset_path':get_user_icons_path(request),
			'icons_list':get_icons_lists(request),
			'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid']}
	return render(request, "./home_page/select_icon.html", context=data)

@login_required
def select_tile(request):
	pc_tile_id=''
	data = {'tile_id':pc_tile_id.strip(),
		 	'user_asset_path':get_user_icons_path(request),
			'icons_list':get_icons_lists(request),
			'APIServer':settings.API_ADRESS, 'userUUID':usersDataStorage.FindDataByUserName(request.user.get_username())['uuid']}
	return render(request, "./home_page/select_tile.html", context=data)



@csrf_exempt
@login_required
def Delete_Icon(request, file_name:str):
	if request.method == 'GET':
		upload_dir = get_user_icons_path(request)
		file_path = os.path.join(upload_dir, file_name)
		if os.path.exists(file_path):
			file_path = os.path.join(upload_dir, file_name)
		print(f'deleted file: {file_path}')
		os.remove(file_path)
		return JsonResponse({'message': f'File deleted {file_name} successfully'}, status=200)
	else:
		return JsonResponse({'error': 'METHOD error. GET awaited'}, status=400)



@csrf_exempt
@login_required
def Upload_Icons(request):
	if request.method == 'POST':
		uploaded_files = request.FILES.getlist('file_name')
		upload_dir = get_user_icons_path(request)  # Путь к папке для сохранения файлов
		
		for file in uploaded_files:
			file_name = file.name
			file_path = os.path.join(upload_dir, file_name)
			
			# Проверяем, существует ли файл с таким именем
			if os.path.exists(file_path):
				# Если файл с таким именем уже существует, генерируем новое имя
				file_name = generate_new_filename(file_path, file_name)
				file_path = os.path.join(upload_dir, file_name)
			
			print(f'save to: {file_path}')
			# Сохраняем файл на сервере
			with open(file_path, 'wb+') as destination:
				for chunk in file.chunks():
					destination.write(chunk)
		
		return JsonResponse({'message': 'Files uploaded successfully'}, status=200)
	else:
		return JsonResponse({'error': 'No files were provided'}, status=400)

def generate_new_filename(upload_dir, filename):
	base_name, extension = os.path.splitext(filename)
	counter = 1
	new_filename = f"{base_name}_{counter}{extension}"
	
	# Пока не найдем уникальное имя файла, добавляем к базовому имени счетчик
	while os.path.exists(os.path.join(upload_dir, new_filename)):
		counter += 1
		new_filename = f"{base_name}_{counter}{extension}"
	
	return new_filename