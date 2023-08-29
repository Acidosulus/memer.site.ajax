import sys
from click import echo, style
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Table, MetaData, and_
from sqlalchemy.orm import Session
from sqlalchemy import Integer,  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Computed, DateTime, ForeignKey, Integer, Table, Text, desc, select
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base, registry
import pprint
from my_library import RowToDict, RowsToDictList, RowsToDictList_last, append_if_not_exists
import math
import datetime
import inspect

#Base = declarative_base()
mapper_registry = registry()
Base = mapper_registry.generate_base()
metadata = Base.metadata


class Book(Base):
	__tablename__ = 'books'

	id_book = Column(Integer, primary_key=True, nullable=False)
	book_name = Column(Text,  nullable=False)
	current_paragraph = Column(Integer, nullable=True)
	user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
	dt = Column(DateTime, nullable=True)

	user = relationship('User')


class Sentence(Base):
	__tablename__ = 'sentences'

	sentence = Column(Text, nullable=False)
	id_book = Column(ForeignKey('books.id_book'), nullable=False)
	id_paragraph = Column(Integer, nullable=False)
	id_sentence = Column(Integer, primary_key=True, nullable=False)

	book = relationship('Book')


class Phrase(Base):
	__tablename__ = 'phrases'

	id_phrase = Column(Integer, primary_key=True, nullable=False)
	phrase = Column(Text, nullable=True)
	translation = Column(Text, nullable=True)
	show_count = Column(Integer, nullable=True)
	ready = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=False)
	last_view = Column(DateTime, nullable=True)
	dt = Column(DateTime, nullable=True)


#t_sqlite_sequence = Table(
#	'sqlite_sequence', metadata,
#	Column(Integer, 'name', NullType),
#	Column(Integer, 'seq', NullType)
#)


class UserWordsLog(Base):
	__tablename__ = 'user_syllable_log'

	user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
	syllable_id = Column(Integer, ForeignKey('syllables.syllable_id'), nullable=False)
	dt = Column(DateTime, nullable=False)
	rowid = Column(Integer, primary_key=True)


class User(Base):
	__tablename__ = 'users'

	user_id = Column(Integer, primary_key=True)
	name = Column(Text, unique=True)
	uuid = Column(Text, unique=True)


class Word(Base):
	__tablename__ = 'words'

	word = Column(Text, nullable=False, unique=True)
	transcription = Column(Text)
	translations = Column(Text)
	examples = Column(Text)
	ready = Column(Integer)
	dt = Column(DateTime)
	notfound = Column(Integer)
	parent_word = Column(Text)
	rowid = Column(Integer, primary_key=True)


class Syllable(Base):
	__tablename__ = 'syllables'

	word = Column(Text, nullable=False, unique=True)
	transcription = Column(Text)
	translations = Column(Text)
	examples = Column(Text)
	show_count = Column(Integer)
	ready = Column(Integer)
	last_view = Column(DateTime)
	syllable_id = Column(Integer, primary_key=True)
	user_id = Column(ForeignKey('users.user_id'))

	user = relationship('User')


class SyllablesParagraph(Base):
	__tablename__ = 'syllables_paragraphs'

	syllable_id = Column(ForeignKey('syllables.syllable_id'), nullable=False)
	example = Column(Text)
	translate = Column(Text)
	sequence = Column(Integer)
	rowid = Column(Integer, primary_key=True, unique=True)

	syllable = relationship('Syllable')



import psycopg2
class LanguageDB:
	# path to sqlite db, autocommit after every update, or manual commint every time you need
	def __init__(self, path:str, autocommit:bool):
		self.autocommit = autocommit
		self.DBparh = path
		#self.DBuri = "sqlite:///"+self.DBparh #"postgresql+psycopg2://postgres:312@185.112.225.153:35432/language" #"sqlite:///"+self.DBparh
		self.DBuri = self.DBparh#"postgresql+psycopg2://postgres:321@185.112.225.153:35432/language"
		self.Base = Base
		self.engine = create_engine(self.DBuri, pool_recycle=30,
                                      			pool_pre_ping=True,
                                      			pool_use_lifo=True)
		#self.meta = MetaData(self.DBuri)
		self.connection = self.engine.connect()
		#self.connection = psycopg2.connect("host='localhost' dbname='language' user='postgres' password='321'")
		self.session = Session(self.engine)
	
	def IfCommit(self):
		if self.autocommit:
			self.session.commit()

	def Drop_all_tables(self):
		tables = [Book, Sentence, Phrase, Syllable, SyllablesParagraph, UserWordsLog, User, Word]
		for table in tables:
			try:
				print(f'	try to drop table: {table.__tablename__}')
				table.__table__.drop(self.engine)
				print('	ok')
			except Exception as e:	
				print(f'		error while drop table: {table.__tablename__}  '+'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'\n\n' + type(e).__name__ +'\n\n' + e.__str__())


	# save book data, return book_id saved record
	def PutBook(self, pbook:Book):
		qr = self.session.query(Book).where(and_(Book.book_name==pbook.book_name, Book.user_id==pbook.user_id))
		if qr.count()==0:
			self.session.add(pbook)
		self.IfCommit()
		return qr.first().id_book
	
	
	def PutSentence(self, pSentence:Sentence):
		qr = self.session.query(Sentence).where(and_(Sentence.id_book == pSentence.id_book, Sentence.sentence == pSentence.sentence))
		if qr.count()==0:
			self.session.add(pSentence)
		self.IfCommit()
		return qr.first().id_paragraph

	# save syllable data, return syllable_id saved record
	def PutSyllabe(self, syllabe:Syllable):
		qr = self.session.query(Syllable).filter(Syllable.word == syllabe.word, Syllable.user_id==syllabe.user_id)
		if qr.count()==0:
			self.session.add(syllabe)
		self.IfCommit()
		return qr.first().syllable_id

	# save 
	def PutSyllablesParagraph(self, sp:SyllablesParagraph):
		qr = self.session.query(SyllablesParagraph).filter(	SyllablesParagraph.syllable == sp.syllable,
							 								SyllablesParagraph.example==sp.example,
															SyllablesParagraph.translate==sp.translate)
		if qr.count()==0:
			self.session.add(sp)
		self.IfCommit()
		return qr.first().rowid


	def GetSyllabe(self, user_id:int, word:str):
		result = self.session.query(Syllable).filter(Syllable.user_id == user_id, Syllable.word == word).first()
		self.IfCommit()
		return result

	
	# upsert user data, return user_id
	def PutUser(self, user:User):
		qr = self.session.query(User).filter(User.name==user.name)
		if qr.count()==0:
			self.session.add(user)
		self.IfCommit()
		return qr.first().user_id


	def PutPhrase(self, phrase:Phrase):
		qr = self.session.query(Phrase).where(Phrase.phrase==phrase.phrase)
		if qr.count()==0:
			self.session.add(phrase)
		self.IfCommit()

	
	# return user books by his name
	def GetUserBooks(self, user_name:str):
		result = RowsToDictList(self.session.query(Book, User).filter(and_(User.name==user_name, User.user_id==Book.user_id)).all())
		for i in range(len(result)):
			result[i]['Min_Paragraph_Number'] = self.GetMinParagraphNumberByBook(user_name, result[i]['id_book'])
			result[i]['Max_Paragraph_Number'] = self.GetMaxParagraphNumberByBook(user_name, result[i]['id_book'])
		return result
	

	# return information about the user book
	def GetUserBookInformation(self, user_name:str, id_book:int):
		result = RowsToDictList(self.session.query(Book, User).filter(and_(User.name==user_name, User.user_id==Book.user_id, Book.id_book==id_book)).first())[0]
		result['Min_Paragraph_Number'] = self.GetMinParagraphNumberByBook(user_name, id_book)
		result['Max_Paragraph_Number'] = self.GetMaxParagraphNumberByBook(user_name, id_book)
		return result

	# return sentenses of paragraph
	def GetUserBookParagraph(self, user_name:str, id_book:int, id_paragraph:int):
		result = RowsToDictList(
								self.session.execute(	select(Sentence).
														where(and_(	User.name==user_name,
																	Book.user_id==User.user_id,
																	Book.id_book==id_book,
																	Sentence.id_book==Book.id_book,
																	Sentence.id_paragraph==id_paragraph,)).
														order_by(Sentence.id_sentence)).all()
								)
		return result

	# retun max paragraph number into book
	def GetMaxParagraphNumberByBook(self, user_name:str, id_book:int):
		result = self.session.query(Book, User, Sentence).filter(and_(		
																		User.name==user_name,
							   											User.user_id==Book.user_id,
																		Book.id_book==id_book,
																		Sentence.id_book==Book.id_book)).order_by(desc(Sentence.id_paragraph)).first()
		return RowsToDictList(result)[2]['id_paragraph']

	# retun min paragraph number into book
	def GetMinParagraphNumberByBook(self, user_name:str, id_book:int):
		result = self.session.query(Book, User, Sentence).filter(and_(		
																		User.name==user_name,
							   											User.user_id==Book.user_id,
																		Book.id_book==id_book,
																		Sentence.id_book==Book.id_book)).order_by(Sentence.id_paragraph).first()
		return RowsToDictList(result)[2]['id_paragraph']


	def GetListOfSyllables(self, user_name:str, ready:int, slice_size:int = 100, slice_number:int = 1):
		print('start GetListOfSyllables:',datetime.datetime.now())
		result = []
		for syllable, user in self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       											User.user_id==Syllable.user_id, 
																				Syllable.ready==ready
																		)).order_by(
																					desc(Syllable.last_view
			  																		)).offset	(
																								slice_size*(slice_number-1
				    																			)).limit(slice_size).all():
			result.append({	'word':syllable.word,
							'transcription':syllable.transcription,
							'translations':syllable.translations,
							'examples':syllable.examples,
							'show_count':syllable.show_count,
							'ready':syllable.ready,
							'last_view':str(syllable.last_view),
							'syllable_id':syllable.syllable_id,
							'user_id':user.user_id,
							'name':user.name,
							'uuid':user.uuid
							})
		self.IfCommit()
		print('end GetListOfSyllables:',datetime.datetime.now())
		return result


	def GetListOfSyllablesByWordPart(self, user_name:str, ready:int, word_part:str, slice_size:int = 100, slice_number:int = 1 ):
		result = []
		for syllable, user in self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       											User.user_id==Syllable.user_id, 
																				Syllable.ready==ready,
																				Syllable.word.contains(word_part)
																		)).order_by(
																					desc(Syllable.last_view
			  																		)).offset	(
																								slice_size*(slice_number-1
				    																			)).limit(slice_size).all():
			result.append({	'word':syllable.word,
							'transcription':syllable.transcription,
							'translations':syllable.translations,
							'examples':syllable.examples,
							'show_count':syllable.show_count,
							'ready':syllable.ready,
							'last_view':str(syllable.last_view),
							'syllable_id':syllable.syllable_id,
							'user_id':user.user_id,
							'name':user.name,
							'uuid':user.uuid
							})
		self.IfCommit()
		return result


	def GetCountOfSyllableSlices(self, user_name:str, ready:int, slice_size:int):
		result = math.ceil(
				self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       											User.user_id==Syllable.user_id, 
																				Syllable.ready==ready)).count()	/slice_size)
		self.IfCommit()
		return result
	
	def GetCountOfUserSyllables(self, user_name:str, ready:int):
		result = self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       							User.user_id==Syllable.user_id, 
																Syllable.ready==ready)).count()
		self.IfCommit()
		return result

	#return full data by the syllable
	def GetSyllable(self, word:str, user_name:str):
		print('start GetSyllable:',datetime.datetime.now())
		print(f'word:{word}  user_name:{user_name}')
		syllable, user = self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
																			User.user_id==Syllable.user_id,
																			Syllable.word == word
																			)).first()
		print(f'syllable.syllable_id:{syllable.syllable_id}')
		result = {			'word':syllable.word,
							'transcription':syllable.transcription,
							'translations':syllable.translations,
							'show_count':syllable.show_count,
							'ready':syllable.ready,
							'last_view':str(syllable.last_view),
							'syllable_id':syllable.syllable_id,
							'user_id':user.user_id,
							'name':user.name,
							'uuid':user.uuid,
							'examples':RowsToDictList(self.session.query(SyllablesParagraph).filter(SyllablesParagraph.syllable_id == syllable.syllable_id).all())
							}
		self.IfCommit()
		print('end GetSyllable:',datetime.datetime.now())
		return result


	def SetSylalbleAsViewed(self, word:str, user_name:str):
		syllable, user = self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       										User.user_id==Syllable.user_id,
																			Syllable.word == word
																			)).first()
		syllable.last_view = datetime.datetime.now()
		syllable.show_count = syllable.show_count + 1
		self.session.commit()
		return {'data':'ok'}


	def GetNextSyllableForLearning(self, user_name:str):
		syllable, user = self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       										User.user_id==Syllable.user_id,
																		    Phrase.ready==0
																			)).order_by(
																						Syllable.last_view
																						).first()
		self.IfCommit()
		return {'data':syllable.word}

	def SetSyllableStatus(self, word:str, user_name:str, status:int):
		syllable, user = self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
								       										User.user_id==Syllable.user_id,
																			Syllable.word == word
																			)).first()
		syllable.ready = status
		self.session.commit()
		return {'data':'ok'}
	

	def GetUsers(self):
		result = RowsToDictList(self.session.query(User).all())
		self.IfCommit()
		return result
	

	def GetPhrases(self, user_name:str, status:int):
		qr = self.session.execute(	select(Phrase, User).
										where(and_(	User.name==user_name, Phrase.ready==status, User.user_id==Phrase.user_id)).
										order_by(Phrase.last_view)).all()
		return RowsToDictList(qr)

	
	def GetPhrase(self, user_name:str, phrase_id:int):
		print(f'user_name:{user_name}       phrase_id:{phrase_id}')
		phrase, user = self.session.execute(	select(Phrase, User).
										where(and_(	User.name==user_name, Phrase.id_phrase==phrase_id, User.user_id==Phrase.user_id)).
										order_by(Phrase.last_view)).first()
		return RowToDict(phrase)


	def SetPhraseStatus(self, phrase_id:int, user_name:str, status:int):
		phrase, user = self.session.query(Phrase, User).filter(and_(		User.name==user_name, 
								       										User.user_id==Phrase.user_id,
																			Phrase.id_phrase == phrase_id
																			)).first()
		phrase.ready = status
		self.session.commit()
		return {'data':'ok'}


	def SetPhraseAsViewed(self, phrase_id:int, user_name:str):
		phrase, user = self.session.query(Phrase, User).filter(and_(		User.name==user_name, 
								       										User.user_id==Phrase.user_id,
																			Phrase.id_phrase == phrase_id
																			)).first()
		phrase.last_view = datetime.datetime.now()
		phrase.show_count = phrase.show_count + 1
		self.session.commit()
		return {'data':'ok'}
	
	def GetNextPhraseForLearning(self, user_name:str):
		phrase, user = self.session.query(Phrase, User).filter(and_(	User.name==user_name, 
								       									User.user_id==Phrase.user_id,
																	    Phrase.ready==0
																		)).order_by(
																						Phrase.last_view
																						).first()
		return RowToDict(phrase)

	def SaveSyllable (self, rq):
		def get_example_by_rowid(id, listofexamples):
			for example in listofexamples:
				if example.rowid==id:
					return example
			return {}
		if rq.syllable_id>0: #we have not zero id, so we must update syllable into DB
			syllable, user = self.session.execute(	select(Syllable, User).
										where(and_(	User.name==rq.username, Syllable.syllable_id==rq.syllable_id))
										).first()
			syllable.word = rq.word
			syllable.transcription = rq.transcription
			syllable.translations = rq.translations
			prnt(RowToDict(syllable))

			paragraphs = self.session.query(SyllablesParagraph).filter(SyllablesParagraph.syllable_id==syllable.syllable_id).all()
			rowids_db_list, rowids_rq_list = [], [] 
			for example in rq.examples:# unique ids from request
				append_if_not_exists(example.rowid, rowids_rq_list)

			for paragraph in paragraphs:# unique ids from db
				append_if_not_exists(paragraph.rowid, rowids_db_list)

			for paragraph in paragraphs: 
				if paragraph.rowid in rowids_rq_list: # save from request to DB if rowid exists
					ex = get_example_by_rowid(paragraph.rowid, rq.examples)
					paragraph.example = ex.example
					paragraph.translate = ex.translate
				if paragraph.rowid not in rowids_rq_list: # paragrath missing into request
					self.session.delete(paragraph)
			
			for example in rq.examples: # add new examples missing into db
				if example.rowid not in rowids_db_list:
					if len(example.example.strip())>0: # only non empty examples
						paragraph = SyllablesParagraph(example = example.example, translate = example.translate, syllable_id = rq.syllable_id)
						self.session.add(paragraph)
		else: # zero syllable_id, we have to insert new data
			user_id_for_request = self.session.query(User).filter(User.name==rq.username).first().user_id
			syllable = Syllable(word = rq.word,
					transcription = rq.transcription,
					translations = rq.translations,
					show_count = 0,
					ready = 0,
					user_id = user_id_for_request)
			self.session.add(syllable)
			self.session.flush()
			self.session.refresh(syllable)
			print(f'Идентификатор вставляемой записи Syllable: {syllable.syllable_id}','\n')
			for example in rq.examples:
				print(f'new example:{example}')
				if len(example.example.strip())>0: # only non empty examples
					paragraph = SyllablesParagraph(	example = example.example, 
				   									translate = example.translate, 
													syllable_id = syllable.syllable_id	)

		self.session.commit()
		return {'data':'ok'}
		
		

		

printer = pprint.PrettyPrinter(indent=12, width=120)
prnt = printer.pprint



if False:
	if sys.platform == 'linux':
		dbn = LanguageDB("postgresql+psycopg2://postgres:321@185.112.225.153:35432/language", autocommit=False)
	else:
		dbn = LanguageDB("postgresql+psycopg2://postgres:321@127.0.0.1:35432/language", False)
	#prnt(dbn.GetUserBooks('admin'))
	prnt(dbn.GetUserBookParagraph('admin',1,7221))
	#prnt(dbn.GetMaxParagraphNumberByBook('admin',1))
	#prnt(dbn.GetMinParagraphNumberByBook('admin',1))
	print('****************************************************************************')
	#prnt(RowsToDictList(dbn.session.query(SyllablesParagraph).filter(SyllablesParagraph.syllable_id == 490).all()))
	#prnt(dbn.GetPhrases('admin',1))
	#prnt(dbn.session.execute(	select(Phrase, User).
	#									where(and_(	User.name=='admin', Phrase.ready==1, User.user_id==Phrase.user_id)).
	#									order_by(Phrase.last_view)).all())
	#RowsToDictList(self.session.query(SyllablesParagraph).filter(SyllablesParagraph.syllable_id == syllable.syllable_id).all())
	print('****************************************************************************')


	#prnt(dbn.GetCountOfUserSyllables('admin',0))
	#prnt(dbn.GetCountOfUserSyllables('admin',1))


##db = LanguageDB("z:\memer.site\language.db", False)
#db = LanguageDB('/run/user/1640202393/media/by-uuid-A8C0-6A35/memer.site/language.db')
##print(db.GetListOSyllables(user_name = 'admin', ready=0, slice_size=100, slice_number=1))
#db = VolumeDB('z:\\memer.site\\')

#db.ShowAllTables()
#echo(style(db.IsFilePathExists('admin', 'Certificate.gif'), fg='bright_cyan'))

#echo(style(db.GetFileText('admin', 'Certificate.gif'), fg='bright_red'))

#echo(style(db.UpdateInsert(user='admin', filepath= 'fractal_background_37_.jpg', comment= 'Второй комментарий' ), fg='bright_white'))

