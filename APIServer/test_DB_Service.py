from my_library import RowToDict, RowsToDictList, append_if_not_exists, delete_non_english_alphabet_characters
from sqlalchemy import Column, Integer, Table, MetaData, and_, func, text, BigInteger
from DB_Service import dbn

def test_is_db_object_initialized():
	assert dbn != None

def test_db_connection_is_live():
	query_result = dbn.session.execute(text(f"""--sql
									select 1 as fld
														;""")).one()[0]
	assert query_result == 1