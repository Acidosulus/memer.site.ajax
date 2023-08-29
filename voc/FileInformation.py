import base64
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django import forms
#import sqlite3 as sl
import datetime
from datetime import date, timedelta
import load_syllable_from_wooordhunt
import os.path
import os
#import subprocess
#import re
#import hashlib
#import threading
import shutil
from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponse
from gtts import gTTS
from django.contrib.auth import authenticate, login, logout
from my_library import delete_non_english_alphabet_characters, sx
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt  
import configparser
import django.http.request
#from requests_toolbelt.multipart import decoder
#from django.utils.encoding import smart_text
import sys
from django.conf import settings
from click import echo, style
from colorama import Fore, Back, Style
# импортируем классы, используемые для определения атрибутов модели
import sqlalchemy
import sqlalchemy.orm
# объект для подключения ядро базы данных
from sqlalchemy.ext.declarative import declarative_base

class FileInformation:
	def __init__(self, file_path:str):
		self.file_path = file_path + '.ini'
		self.txt = ''
		self.config = configparser.ConfigParser()
		if not os.path.isfile(self.file_path):
			self.txt = os.path.splitext(file_path)[0]
			file_path
		else:
			self.config.read(self.file_path)
			try:
				self.txt = self.config["file"]["txt"].strip()
			except: pass
			
	def WriteState(self):
		self.config["file"]= {"txt":self.txt}
		file = open(self.file_path, 'w', encoding="UTF-8")
		self.config.write(file)
		file.close


def listdir_croppath(startdir):
	paths = listdir_fullpath(startdir)
	result = []
	for path in paths:
		result.append(path[len(startdir):])
	return result


def listdir_fullpath(startdir):
	result = []
	for top, dirs, files in os.walk(startdir):
		for nm in dirs:
			cdir = os.path.join(top, nm)
			if cdir not in result:
				result.append(cdir)
	return result


#print(listdir_fullpath('D:\\memer.site\\Storage\\admin\\media'))
#print('===========')
#print(listdir_croppath('D:\\memer.site\\Storage\\admin\\media'))



#fi = FileInformation('/run/user/1640202393/media/by-uuid-A8C0-6A35/memer.site/voc/constants.py')
#print(fi.txt)
##fi.WriteState()