import base64
#import sqlite3 as sl
import datetime
from datetime import date, timedelta
import os.path
import os
#import subprocess
#import re
#import hashlib
#import threading
import shutil
from my_library import delete_non_english_alphabet_characters, sx
from pathlib import Path
import configparser
import django.http.request
#from requests_toolbelt.multipart import decoder
#from django.utils.encoding import smart_text
import sys
from click import echo, style
from colorama import Fore, Back, Style
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table, MetaData, select, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = sqlalchemy.orm.declarative_base()

class VolumeDB:
	def __init__(self, path:str):
		
		self.DBparh = os.path.join(path, 'userdata.db')
		self.DBuri = f'sqlite:///{self.DBparh}'
		self.Base = automap_base()
		self.engine = create_engine(url=self.DBuri ) #, echo=True
		self.Base.prepare(self.engine, reflect=True)
		self.meta = MetaData(self.DBuri)
		self.connection = self.engine.connect()
		self.session = Session(self.engine)
		
		self.Files = self.Base.classes.file		
		

	# print all data from all tables of database
	def ShowAllTables(self):
		sqr = self.session.query(self.Files)
		for row in sqr:
			echo(style(str(row.id) +'   '+ str(row.user) +'   '+ str(row.path) +'   '+ str(row.text), fg='bright_yellow'))

	# return id filepath from DB, if path not exists then return -1
	def IsFilePathExists(self, User:str, Path:str):
		sqr = self.session.query(self.Files).filter(and_(self.Files.path == Path, self.Files.user == User ))
		return (-1 if sqr.count()==0 else sqr.first().id)
		
	# verify is record about file is in database then update it, but insert if don't
	def UpdateInsert(self, user:str, filepath:str, comment:str):
		filepath = filepath.replace('|','\\').replace('\\\\','\\').replace('\\', '/')
		record_id = self.IsFilePathExists(User=user, Path=filepath)
		if record_id == -1:
			self.session.add(self.Files(user = user, path = filepath, text=comment))
		else:
			file = self.session.query(self.Files).filter(self.Files.id==record_id).first()
			file.path = filepath; file.text = comment; file.user=user
		self.session.commit()
		pass

	# return text bind with filepath from DB, elsewhere return empty string
	def GetFileText(self, User:str, Path:str):
		result = self.session.query(self.Files).filter(and_(self.Files.user==User, self.Files.path==Path)).first()
		return (result.text if result is not None else '')

#db = VolumeDB('/run/user/1640202393/media/by-uuid-A8C0-6A35/memer.site')
#db = VolumeDB('z:\\memer.site\\')

#db.ShowAllTables()
#echo(style(db.IsFilePathExists('admin', 'Certificate.gif'), fg='bright_cyan'))

#echo(style(db.GetFileText('admin', 'Certificate.gif'), fg='bright_red'))

#echo(style(db.UpdateInsert(user='admin', filepath= 'fractal_background_37_.jpg', comment= 'Второй комментарий' ), fg='bright_white'))

