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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import select

#database_dir = os.path.abspath(os.path.dirname(__file__))
#database_uri = f'sqlite:///{database_dir}/userdata.db'

#Session = sessionmaker()
#engine = create_engine(database_uri)
#session = Session(bind=engine)


Base = sqlalchemy.orm.declarative_base()


class File(Base):
	__tablename__ = 'file'
	id =   sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
	path = sqlalchemy.Column(String,  nullable=False)
	text = sqlalchemy.Column(String,  nullable=True)

	def __repr__(self):
		return f'<file id={self.id} path="{self.path}" text="{self.text}">'



class VolumeDB:
	def __init__(self, path:str):
		self.DBparh = os.path.join(path, 'userdata.db')
		#print('===============>'+self.DBparh)
		self.DBuri = f'sqlite:///{self.DBparh}'
		self.engine = create_engine(url=self.DBuri)
		if not os.path.isfile(self.DBparh):
			Base.metadata.create_all(self.engine)
		self.Session = sessionmaker()
		
		self.session = self.Session(bind=self.engine)
	
	# print all data from all tables of database
	def ShowAllTables(self):
		sqr = self.session.query(File).all()
		for row in sqr:
			echo(style(row, fg='bright_yellow'))

	# return id filepath from DB, if path not exists then return -1
	def IsFilePathExists(self, pPath:str):
		sqr = self.session.query(File).filter(File.path == pPath)
		return (-1 if sqr.count()==0 else sqr.first().id)
		
	# verify is record about file is in database then update it, but insert if don't
	def UpdateInsert(self, filepath:str, comment:str):
		pfile = File(path = filepath, text = comment)
		record_id = self.IsFilePathExists(pfile.path)
		if record_id == -1:
			self.session.add(pfile)
		else:
			file = self.session.query(File).filter(File.id==record_id).first()
			file.path = pfile.path; file.text = pfile.text
		self.session.commit()
		pass

	# return text bind with filepath from DB, elsewhere return empty string
	def GetFileText(self, pPath:str):
		result = self.session.query(File).filter(File.path==pPath).first()
		return (result.text if result is not None else '')

#db = VolumeDB('/run/user/1640202393/media/by-uuid-A8C0-6A35/memer.site')

#db.GetFileText('Certificate.gif')
#db.GetFileText('Certificate1s.gif')

#db.ShowAllTables()

#echo(style(db.IsFilePathExists('Certificate.gif'), fg='bright_cyan'))

#db.UpdateInsert(File(path = 'Certificate.gif',text = 'Первый комментарий' ))

#db.UpdateInsert(File(path = 'Certificate.gif',text = 'Первый комментарий' ))

#db.UpdateInsert(File(path = 'Certificate1.gif',text = 'Второй комментарий' ))

