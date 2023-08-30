from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django import forms
from datetime import date, timedelta
import os
from my_library import delete_non_english_alphabet_characters, sx
from pathlib import Path
from django.conf import settings
from click import echo, style
from colorama import Fore, Back, Style
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table, MetaData, select, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from my_library import *


class LanguageDBLast:
	def __init__(self, path:str):
		self.DBparh = path #os.path.join(path, 'language.db')
		self.DBuri = f'sqlite:///{self.DBparh}'
		self.Base = automap_base()
		self.engine = create_engine(url=self.DBuri )
		
		self.Base.prepare(autoload_with=self.engine)
		#self.Base.prepare(engine = self.engine, reflect=True)
		self.meta = MetaData(self.DBuri)
		self.connection = self.engine.connect()
		self.session = Session(self.engine)
		#print(dir(self.Base.classes))
		#self.Users 					= self.Base.classes.users
		#self.Words 					= self.Base.classes.words
		self.Syllable				= self.Base.classes.vocapp_syllable
		self.Users					= self.Base.classes.auth_user
		self.Phrases				= self.Base.classes.vocapp_phrases
		self.Books					= self.Base.classes.vocapp_books
		self.Paragraphs				= self.Base.classes.vocapp_paragraphs
		#self.Syllables_paragraphs 	= self.Base.classes.syllables_paragraphs
	
	
	def GetAllSyllables(self):
		return RowsToDictList(self.session.query(self.Syllable).all())

	def GetSyllable(self, pword:str):
		rows = self.session.query(self.Syllable).filter(self.Syllable.word==pword).all()
		return RowToDict(rows[0])

	def GetAllUsers(self):
		return RowsToDictList(self.session.query(self.Users).all())

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



#db = LanguageDB("y:\\1640202393\\media\\by-uuid-A8C0-6A35\\memer.site\\language.db")
#db = LanguageDBLast('/run/user/1640202393/media/by-uuid-A8C0-6A35/memer.site/voc/db.sqlite3')
#print(db.GetAllUsers())
#print(GetDividedExamples(db.GetSyllable('mend')['examples']))



#for row in db.session.query(db.Syllables).all():
#	print(row.word)
#db = VolumeDB('z:\\memer.site\\')

#db.ShowAllTables()
#echo(style(db.IsFilePathExists('admin', 'Certificate.gif'), fg='bright_cyan'))

#echo(style(db.GetFileText('admin', 'Certificate.gif'), fg='bright_red'))

#echo(style(db.UpdateInsert(user='admin', filepath= 'fractal_background_37_.jpg', comment= 'Второй комментарий' ), fg='bright_white'))

