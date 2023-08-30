import base64
import datetime
from datetime import date, timedelta
import os
from my_library import *
from pathlib import Path
import sys
from click import echo, style
from colorama import Fore, Back, Style
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table, MetaData, select, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from DBLastRead import *
from DB_Service import *
import pprint
import uuid


printer = pprint.PrettyPrinter(indent=4)

if sys.platform == 'linux':
	dbl = LanguageDBLast(r'/run/user/1640202393/media/by-uuid-A8C0-6A35/memer.site/voc/db.sqlite3')
	dbn = LanguageDB("postgresql+psycopg2://postgres:321@185.112.225.153:35432/language", autocommit=False)
else:
	dbl = LanguageDBLast(r'z:\memer.site\voc\db.sqlite3')
	dbn = LanguageDB(r'z:\memer.site\language.db', False)
print('Drop database tables')
dbn.Drop_all_tables()
print('Create database tables')
dbn.Base.metadata.create_all(bind=dbn.engine)



for user in dbl.GetAllUsers():
	printer.pprint(user)
	dbn.PutUser(User(name=user['username'], uuid=str(uuid.uuid4())))
	dbn.session.commit()





print('\n\n')

for lphrase in RowsToDictList(dbl.session.query(dbl.Phrases).all()):
	printer.pprint(lphrase)
	dbn.PutPhrase(	Phrase(		phrase=lphrase['phrase'],
								translation=lphrase['translation'],
								show_count = lphrase['show_count'],
								ready=lphrase['ready'],
								user_id=lphrase['userid'],
								last_view=lphrase['last_view'],
								dt=lphrase['dt']
								))
dbn.session.commit()


for lbook in RowsToDictList(dbl.session.query(dbl.Books).all()):
	lbook['dt'] = lbook['dt'] if lbook['dt']!='None' else datetime.datetime.now()
	#print('================', lbook['dt'], lbook['dt']!=None)
	printer.pprint(lbook)
	book_id = dbn.PutBook( Book( 	book_name = str(lbook['book_name']),
						current_paragraph = str(lbook['current_paragraph']),
						user_id = int(lbook['userid']),
						dt = lbook['dt']
						))
	for counter, lparagraph in enumerate(RowsToDictList(dbl.session.query(dbl.Paragraphs).where(dbl.Paragraphs.id_book==lbook['id_book']).all())):
		printer.pprint(lparagraph)
		print('\n')
		sentenses = split_pharagraf_on_sentences(lparagraph['paragraph'])
		printer.pprint(sentenses)
		for sentense in sentenses:
			dbn.PutSentence(Sentence(	id_paragraph=lparagraph['id_paragraph'],
										sentence = sentense,
										id_book = book_id))

dbn.session.commit()

for number, syllable in enumerate(dbl.GetAllSyllables()):
	print(number)
	printer.pprint(syllable)
	syl = Syllable(	word = syllable['word'],
					transcription = syllable['transcription'],
					translations = syllable['translations'],
					show_count = syllable['show_count'],
					ready = syllable['ready'],
					last_view = syllable['last_view'],
					user_id = 1)
	syl_id = dbn.PutSyllabe(syl)
	
	print(syl_id,'\n')
	print(syllable['examples'],'\n\n')
	examples = GetDividedExamples(syllable['examples'])
	for example in examples:
		if len(example['example'])==0: continue
		sp = SyllablesParagraph(syllable=dbn.session.query(Syllable).filter(Syllable.syllable_id==syl_id).first(),
								example=example['example'],
								translate=example['translate'] )
		dbn.PutSyllablesParagraph(sp)
	

	
	dbn.session.commit()
