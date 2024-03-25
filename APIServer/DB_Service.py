import sys
from click import echo, style
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Table, MetaData, and_, func, text, BigInteger
from sqlalchemy.orm import Session
from sqlalchemy import Integer,  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Computed, DateTime, ForeignKey, Integer, Table, Text, desc, select, update
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base, registry
import pprint
from my_library import RowToDict, RowsToDictList, append_if_not_exists, delete_non_english_alphabet_characters
import math
import datetime
import inspect
from settings import Options

from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import concat

options = Options('options.ini')

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

class ReadingJournal(Base):
	__tablename__ = 'reading_journal'
	
	row_id = Column(Integer, primary_key=True, nullable=False)
	user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
	id_paragraph = Column(Integer,ForeignKey('sentences.id_paragraph'), nullable=False)
	id_book = Column(ForeignKey('books.id_book'), nullable=False)
	dt = Column(DateTime, nullable=True)


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


class HPTile(Base):
    __tablename__ = 'hp_tiles'

    tile_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    hyperlink = Column(Text)
    onclick = Column(Text)
    icon = Column(Text, nullable=False)
    color = Column(Text)
    tile_index = Column(Integer)

class HPPlank(Base):
    __tablename__ = 'hp_planks'

    plank_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plank_name = Column(Text, nullable=False)
    index = Column(Integer, default=0, nullable=False)

class HPRow(Base):
    __tablename__ = 'hp_rows'

    row_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    row_name = Column(Text, nullable=False)
    row_type = Column(Integer, default=0, nullable=False)
    row_index = Column(Integer, default=0, nullable=False)
    plank_id = Column(Integer, ForeignKey('hp_planks.plank_id'), default=0, nullable=False)
    plank = relationship("HPPlank", backref="rows")



class HpRowTile(Base):
    __tablename__ = 'hp_row_tiles'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    row_id = Column(BigInteger, nullable=False)
    tile_id = Column(BigInteger, nullable=False)


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
		return int(RowsToDictList(result)[2]['id_paragraph'])

	# retun min paragraph number into book
	def GetMinParagraphNumberByBook(self, user_name:str, id_book:int):
		result = self.session.query(Book, User, Sentence).filter(and_(		
																		User.name==user_name,
							   											User.user_id==Book.user_id,
																		Book.id_book==id_book,
																		Sentence.id_book==Book.id_book)).order_by(Sentence.id_paragraph).first()
		return int(RowsToDictList(result)[2]['id_paragraph'])


	def GetListOfSyllables(self, user_name:str, ready:int, slice_size:int = 100, slice_number:int = 1):
		print('start GetListOfSyllables:',datetime.datetime.now())
		result = []
		for syllable, user in self.session.query(Syllable, User).filter(and_(	User.name==user_name, 
									  											User.user_id==Syllable.user_id, 
																				Syllable.ready==ready
																		)).order_by(
																					Syllable.last_view
			  																		).offset	(
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


	def SaveBookPosition(self, user_name:str, id_book:int, new_current_paragraph:int):
		if self.GetMinParagraphNumberByBook(user_name, id_book) <= new_current_paragraph <= self.GetMaxParagraphNumberByBook(user_name, id_book):
			self.session.execute(	update(Book).
														where(and_(	Book.user_id==self.GetUserId(user_name),
																	Book.id_book==id_book)).
														values(	current_paragraph = new_current_paragraph,
					 											dt = datetime.datetime.now()))
			self.session.commit()
			self.SaveBookReadingData( self.GetUserId(user_name), id_book, new_current_paragraph)
			result = {'data':'Ok'}
		else:
			result = {'data':'ERROR: New current paragraph is outside of book paragraph range.'}
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

	def GetCountOfUserSyllablesWorkedOutToday(self, user_name:str):
		#current_user_id = self.session.query(User).filter(User.name==user_name). first().user_id
		result = self.session.query(UserWordsLog, User).filter(and_(	User.name==user_name, 
									  									User.user_id==UserWordsLog.user_id,
																		UserWordsLog.dt>=datetime.datetime.now() - datetime.timedelta(days=1)
																		)).count()
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
		syllable = self.session.query(Syllable).filter(and_(				Syllable.user_id == self.GetUserId(user_name),
																			Syllable.word == word
																			)).first()
		view_time = datetime.datetime.now()
		syllable.last_view = view_time
		syllable.show_count = syllable.show_count + 1

		wordslog = UserWordsLog(	user_id=self.GetUserId(user_name),
									syllable_id=syllable.syllable_id,
									dt=view_time)
		self.session.add(wordslog)

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
		syllable = self.session.query(Syllable).filter(and_(				Syllable.user_id==self.GetUserId(user_name),
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
		print(f'user_name:{user_name}	  phrase_id:{phrase_id}')
		if phrase_id>0:
			phrase, user = self.session.execute(	select(Phrase, User).
													where(and_(	User.name==user_name, Phrase.id_phrase==phrase_id, User.user_id==Phrase.user_id)).
													order_by(Phrase.last_view)).first()
			return RowToDict(phrase)
		else: return {'id_phrase':0, 'phrase':'', 'translation':''}


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


	def SavePhrase(self, user_name, phrase_id, text, translate):
		ln_user_id = self.GetUserId(user_name)
		if ln_user_id>0:
			if phrase_id>0:
				try:
					phrase = self.session.query(Phrase).filter(and_(	Phrase.id_phrase == phrase_id,
																		Phrase.user_id == ln_user_id)).first()
					prnt(RowToDict(phrase))
					phrase.phrase = text
					phrase.translation = translate
					phrase.last_view = datetime.datetime.now()
					self.session.commit()
					return {"status":"ok"}
				except:
					return {"status":"error - data has not saved"}
			else: #it's a new phrase
				try:
					self.session.add(Phrase(phrase=text, translation = translate, user_id = ln_user_id, last_view = datetime.datetime.now(), dt=datetime.datetime.now(), ready=0, show_count=0))
					self.session.commit()
					return {"status":"ok"}
				except: return {"status":"error - data has not added"}
		else:
			return {"status":"error - wrong user name"}



	def SaveSyllable (self, rq):
		def get_example_by_rowid(id, listofexamples):
			for example in listofexamples:
				if example.rowid==id:
					return example
			return {}
		print(f'rq.syllable_id from request:{rq.syllable_id}')
		qr = self.session.query(Syllable).filter(	and_(	
													   								Syllable.user_id==self.GetUserId(rq.username),
																					Syllable.word==rq.word
																		)).first()
		rq.syllable_id = (-1 if qr is None else int(RowToDict(qr)['syllable_id']))
		print(f'rq.syllable_id from DB:{rq.syllable_id}')
		if rq.syllable_id>0: #we have not zero id, so we must update syllable into DB
			syllable, user = self.session.execute(	select(Syllable, User).
										where(and_(	User.name==rq.username, 
					 								User.user_id == Syllable.user_id,
					 								Syllable.syllable_id==rq.syllable_id,
													))
										).first()
			syllable.word = rq.word
			syllable.transcription = rq.transcription
			syllable.translations = rq.translations
			syllable.last_view = datetime.datetime.now()
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
					user_id = user_id_for_request,
					last_view=datetime.datetime.now())
			self.session.add(syllable)
			self.session.flush()
			self.session.refresh(syllable)
			print(f'Идентификатор вставляемой записи Syllable: {syllable.syllable_id}','\n')
			for example in rq.examples:
				print(f'new example: {example}')
				if len(example.example.strip())>0: # only non empty examples
					paragraph = SyllablesParagraph(	example = example.example, 
				   									translate = example.translate, 
													syllable_id = syllable.syllable_id	)
					self.session.add(paragraph)
					self.session.flush()
					self.session.refresh(paragraph)
					print(f'new paragraph: {RowToDict(paragraph)}')
		self.session.commit()
		return {'data':'ok'}
	# return user ID by user name		
	def GetUserId(self, user_name:str):
		user = self.session.execute(	select(User).
										where(	User.name==user_name)
										).first()

		return user[0].user_id
	
	# return list of learning words from book paragraphs list
	def GetListOfUserSyllableFromParagraphsId(self, user_name:str, id_book:int, paragraph_ids_list:list):
		words_list = []
		for paragraph_id in paragraph_ids_list:
			for sentence in self.GetUserBookParagraph(user_name, int(id_book), int(paragraph_id)):
				for word in sentence['sentence'].strip().split(' '):
					word_candidate = delete_non_english_alphabet_characters(word)
					if len(word_candidate)>2:
						append_if_not_exists(word_candidate.lower(), words_list)
		result = []
		for element in self.session.query(Syllable.word).filter(and_(		Syllable.user_id==self.GetUserId(user_name),
																			Syllable.ready==0,
																			Syllable.word.in_(words_list))).all():
			append_if_not_exists(element[0], result)
		return result


	def GetLasReadedBookByUser(self, user_name:str):
		return self.session.query(Book.id_book).filter(Book.user_id == self.GetUserId(user_name)).order_by(Book.dt.desc()).first()[0]


	def SaveBookReadingData(self, id_user, id_book, id_paragraph):
		self.session.add( ReadingJournal( 	user_id = id_user,
										  			id_book = id_book,
													id_paragraph = id_paragraph,
													dt = datetime.datetime.now() ))
		self.session.commit()


	def GetTodayReadingParagraphs(self, user_name):
		return self.session.execute(text(f"""--sql
								   			select sum(diff)
												from (
														SELECT id_book, max(id_paragraph) - min(id_paragraph) as diff
														FROM public.reading_journal
														WHERE dt >= CURRENT_TIMESTAMP - INTERVAL '1 day' and user_id = {self.GetUserId(user_name)}
														group by id_book ) as ct
														;""")).one()[0]


	def SaveTile(self, tile_id, user_name, name, hyperlink, icon, color):
		print('SaveTile:', tile_id, user_name, name, hyperlink, icon)
		ln_user_id = self.GetUserId(user_name)
		tile = self.session.query(HPTile).filter(and_(	HPTile.user_id == ln_user_id,
									   		HPTile.tile_id == tile_id)).first()
		if tile is None:
			self.session.add(HPTile(	user_id = ln_user_id,
			  			name = name,
						hyperlink = hyperlink,
				  		icon = icon,
				    	color = color))
			self.session.commit()
			return {"status":"ok - added"}
		else:
			tile.name = name
			tile.hyperlink = hyperlink
			tile.icon = icon
			tile.color = color
			self.session.commit()
			return {"status":"ok - updated"}

	def GetTiles(self, user_name):
		print(f'GetTiles: user_name = "{user_name}"')
		ln_user_id = self.GetUserId(user_name)
		tiles = self.session.query(HPTile).filter(HPTile.user_id == ln_user_id).all()
		tiles = RowsToDictList(tiles)
		return tiles

	def GetTile(self, user_name, tile_id):
		print(f'GetTile: user_name = "{user_name}", tile_id: {tile_id}')
		ln_user_id = self.GetUserId(user_name)
		tile = self.session.query(HPTile).filter(	HPTile.user_id == ln_user_id,
								   			HPTile.tile_id == tile_id).first()
		return RowToDict(tile)
  
	def DeleteTiles(self, user_name, tile_id):
		print(f'DeleteTiles: user_name = "{user_name}", tile_id = {tile_id}')
		ln_user_id = self.GetUserId(user_name)
		self.session.query(HPTile).filter(HPTile.user_id == ln_user_id, HPTile.tile_id == tile_id).delete()
		self.session.commit()
		return True

	def GetRows(self, user_name:str):
		print(f'GetRows: user_name = "{user_name}"')
		ln_user_id = self.GetUserId(user_name)
		rows = self.session.query(HPRow).filter(	HPRow.user_id == ln_user_id).all()
		return RowsToDictList(rows)

	def GetRow(self, user_name:str, row_id:int):
		print(f'GetRow: user_name = "{user_name}", "{row_id}"')
		ln_user_id = self.GetUserId(user_name)
		row = RowToDict(self.session.query(HPRow).filter(	HPRow.user_id == ln_user_id,
								  					HPRow.row_id == int(row_id)).first())
		tiles = RowsToDictList(self.session.query(HPTile).filter(	HPRow.row_id == int(row_id),
                                            		HPTile.tile_id == HpRowTile.tile_id).all())
		row['tiles'] = tiles
		return row

	def GetHPRowData(self, user_name:str, row_id):
		print(f'GetHPRowData: user_name = "{user_name}", "{row_id}"')
		ln_user_id = self.GetUserId(user_name)
		row = RowToDict(self.session.query(HPRow).filter(	HPRow.user_id == ln_user_id,
								  					HPRow.row_id == int(row_id)).first())
		tiles = RowsToDictList(self.session.query(HPTile).filter(	HPRow.row_id == int(row_id),
                                            		HPTile.tile_id == HpRowTile.tile_id).all())
		row['tiles'] = tiles
		return row

# class HPRow(Base):
#	__tablename__ = 'hp_rows'
#	row_id = Column(Integer, primary_key=True)
#	user_id = Column(Integer, nullable=False)
#	row_name = Column(Text, nullable=False)
#	row_type = Column(Integer, default=0, nullable=False)
#	row_index = Column(Integer, default=0, nullable=False)
#	plank_id = Column(Integer, ForeignKey('hp_planks.plank_id'), default=0, nullable=False)
#	plank = relationship("HPPlank", backref="rows")

  
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


if True:
	if sys.platform == 'linux':
		dbn = LanguageDB(options.LANDDBURI, autocommit=False)
		# prnt(dbn.GetHPRowData('admin', 1))
	else:
		dbn = LanguageDB(options.LANDDBURI, autocommit=False)
		#print(f"GetTodayReadingParagraphs: {dbn.GetTodayReadingParagraphs('admin')}")
	#print(dbn.SavePhrase('admin',0, 'delme', 'удали меня'))
	#prnt(dbn.GetUserBooks('admin'))
	#prnt(dbn.GetUserId('admin'))
	#prnt(dbn.SaveBookPosition('admin',1,7212))
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

