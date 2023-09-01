import os.path
from collections.abc import Iterable

# если символ русский то он заменяется на номер буквы в алфавите обёрнутой %3c %3e
def code_char (pc_char:str):
	lc_result = 0
	if pc_char == pc_char.lower(): lb_mini_flag = True
	else: lb_mini_flag = False
	if pc_char == 'а':
		lc_result = 1
	if pc_char == 'б':
		lc_result = 2
	if pc_char == 'в':
		lc_result = 3
	if pc_char == 'г':
		lc_result = 4
	if pc_char == 'д':
		lc_result = 5
	if pc_char == 'е':
		lc_result = 6
	if pc_char == 'ё':
		lc_result = 7
	if pc_char == 'ж':
		lc_result = 8
	if pc_char == 'з':
		lc_result = 9
	if pc_char == 'и':
		lc_result = 10
	if pc_char == 'й':
		lc_result = 11
	if pc_char == 'к':
		lc_result = 12
	if pc_char == 'л':
		lc_result = 13
	if pc_char == 'м':
		lc_result = 14
	if pc_char == 'н':
		lc_result = 15
	if pc_char == 'о':
		lc_result = 16
	if pc_char == 'п':
		lc_result = 17
	if pc_char == 'р':
		lc_result = 18
	if pc_char == 'с':
		lc_result = 19
	if pc_char == 'т':
		lc_result = 20
	if pc_char == 'у':
		lc_result = 21
	if pc_char == 'ф':
		lc_result = 22
	if pc_char == 'х':
		lc_result = 23
	if pc_char == 'ц':
		lc_result = 24
	if pc_char == 'ч':
		lc_result = 25
	if pc_char == 'ш':
		lc_result = 26
	if pc_char == 'щ':
		lc_result = 27
	if pc_char == 'ъ':
		lc_result = 28
	if pc_char == 'ы':
		lc_result = 29
	if pc_char == 'ь':
		lc_result = 30
	if pc_char == 'э':
		lc_result = 31
	if pc_char == 'ю':
		lc_result = 32
	if pc_char == 'я':
		lc_result = 33
	lc_result = lc_result if lb_mini_flag else lc_result+100
	return '%5B'+str(lc_result)+'%5D'

#для русского символа возвращает истину
def is_char_russian(pc_char:str):
	if pc_char.lower() in 'ёйцукенгшщзхъфывапролджэячсмитьбю': return True
	else: return False

# кодирует строку, заменяя в ней русские символы безопасным образом
def Code_string(pc_str:str):
	lc_str = ''
	for lc_char in pc_str:
		if is_char_russian(lc_char):
			lc_str = lc_str + code_char(lc_char)
		else:
			lc_str = lc_str + lc_char
	return lc_str


# обращает прайс в csv файле в обратном порядке, чтобы когда при загрузке в торговую систему он будет ей обращен - порядок стал бы таким каким был на сайте поставщика
def reverse_csv_price(lc_source_file_name:str):
	source_file = open(lc_source_file_name, mode='r', encoding='cp1251')
	lines = source_file.read().splitlines()
	source_file.close()
	inverted_file = open(lc_source_file_name+'_reversed.csv', mode='w', encoding='cp1251')
	inverted_file.writelines(lines[0] + '\n')
	for i in reversed(lines[1:len(lines)]):
		inverted_file.write(i + '\n')
	inverted_file.close()


def delete_from_string_between_substrings(lc_source: str, lc_from: str, lc_to: str):	# удаляет подстроку из строки ограниченную начальной и конечной подстрокой
	l = lc_source.find(lc_from)
	r = lc_source.find(lc_to)
	if l > -1 and r > -1: return lc_source[:l] + lc_source[r + 1:-1]
	else: return lc_source

def file_to_str(file_path:str):		 # считывает текстовый файл в строку
	with open(file_path, "r", encoding="utf-8") as myfile:
		data = ' '.join(myfile.readlines())
	myfile.close()
	return data


def prepare_for_csv_non_list (pc_value):	 # подготовка к записи в csv, списки преобразуются к строке с разделителями пробелами
	if type(pc_value) =="<class 'str'>":
		return prepare_str(pc_value)
	else:	#if type(pc_value) == "<class 'list'>"
		lc = ''
		for i in pc_value:
			lc = lc + ' ' + prepare_str(i)
		return lc.strip()
	return pc_value


def prepare_for_csv_list(pc_value):	 # подготовка к записи в csv, списки преобразуются в список с разделителями точка с запятой и экранируются кавычками
	if type(pc_value) == "<class 'str'>":
		return prepare_str(pc_value)
	else: #if type(pc_value) == "<class 'list'>"
		lc = ''
		ln_counter = 0
		for i in pc_value:
			ln_counter=ln_counter+1
			if ln_counter != 1: lc_comma = ';'
			else: lc_comma = ''
			lc = lc + lc_comma + prepare_str(i)
		return '"'+lc.strip()+'"'

def prepare_str(pc_value:str):  #удаляет из будущего параметра CSV недопустимые символы
	return pc_value.replace('"','').replace(';',' ').replace('\n',' ').replace('\t',' ')

def sx(source_string='', left_split='', right_split='', index=1):
	# print(source_string + ' '+left_split + ' '+ right_split)
	# print(index)
	# star_position = 0
	# print('')
	# print(source_string.count(left_split))
	if source_string.count(
			left_split) < index:  # если требуется вхождение с большим номером чем имеется в исходной строке
		return ""
	lc_str = source_string
	for i in range(0, index):  # range(1,source_string.count(left_split)):
		lc_str = lc_str[lc_str.find(left_split) + len(left_split):len(lc_str)]
		# print(lc_str)
	# print(lc_str[0:lc_str.find(right_split)])
	return lc_str[0:lc_str.find(right_split)]

def is_price_have_link(price_path:str, price_link:str): #возвращает истину, если ссылка на сайт поставшика уже присустствует в прайсе
		lb_result = False
		try:
			price_file = open(price_path, mode='r', encoding='cp1251')
			lc_str = price_file.read()
			price_file.close()
			lb_result = True if lc_str.count(price_link)>0 else False
		except: lb_result = False
		return lb_result



class Price:
	def __init__(self, file_name:str):
		if os.path.isfile(file_name):
			self.good = []
			self.goods = []
		else:
			self.good = []
			self.goods = []
			self.goods.append(['ID товара', 'наименование', 'описание', 'цена', 'орг %', 'ccылка на товар на сайте поставщика', 'ссылки на Фото', 'размер'])

	def add_good(self, id, name, descr, price, procent, link_on_site, link_on_pictures, size):
		self.goods.append([id, name, descr, price, procent, link_on_site, link_on_pictures, size])

	def write_to_csv(self, file_name):
		if os.path.isfile(file_name):
			#self.goods.pop(0) # удаляем заголовок списка, если будем дополнять существующий прайс
			file = open(file_name, mode='a', encoding='cp1251')
		else:
			file = open(file_name, mode='w', encoding='cp1251')

		for gd in self.goods:
			lc_str = ''
			for col in gd:
				if col != None:
					lc_str = lc_str + col + ';'
				else:
					lc_str = lc_str + ';'
			file.write((lc_str+'|').replace(';|', '').replace('|', '') + '\n')
		file.close()
		self.goods.clear()


def delete_non_english_alphabet_characters(lc_string:str):
	lc_engilsh_simbols = "qwertyuiopasdfghjklzxcvbnm"
	lc_engilsh_simbols = lc_engilsh_simbols + lc_engilsh_simbols.upper() + "'"
	lc_result = ''
	for character in lc_string:
		if character in lc_engilsh_simbols:
			lc_result += character
	return lc_result


# return one row query result as dict
def RowToDict(row):
	result = {}
	for column in row.__table__.columns:
		result[column.name] = str(getattr(row, column.name))
	return result

# returl query result as dict list


def RowsToDictList(rows):
	result = []
	for row in rows:
		dic = {}
		if isinstance(row, Iterable):
			for element in row:
				dic = {**dic, **RowToDict(element)}
			result.append(dic)
		else:
			result.append(RowToDict(row))
	return result


# returl query result as dict list
def RowsToDictList_last(rows):
	result = []
	for row in rows:
		result.append(RowToDict(row))
	return result

# divide examples str to dict list
def GetDividedExamples(source:str):
	#print(source)
	lc_examples_html = source
	if lc_examples_html[-2:]!=chr(13)+chr(10):
		lc_examples_html = lc_examples_html + chr(13)+chr(10)
		if lc_examples_html[-2:] != chr(13) + chr(10):
			lc_examples_html = lc_examples_html + chr(13) + chr(10)
	paragraphs = lc_examples_html.split(chr(13)+chr(10)+chr(13)+chr(10))
	result = []
	for part in paragraphs:
		ll_example = part.split('\n')
		
		try:str_example = ll_example[0]
		except:str_example = ''

		try:str_translate = ll_example[1]
		except:str_translate = ''

		result.append({'example':str_example, 'translate':str_translate})
	return result

def get_background_color(idx:int):
	ll = ["#1C1C1C","#181513","#140F0B","#1E1112","#121910","#230D21","#022027","#16251C","#270A1F","#320A18","#131313","#1B1116","#1D1E33","#282828","#151719","#002137",
		  "#35170C","#321011","#232C16","#302112","#1A162A","#32221A","#464544","#452D35","#1E1E1E","#343E40","#212121","#412227","#3B3C36","#23282B","#18171C","#141613",
		  "#1F0E11","#1D1018","#161A1E","#0A0A0A"]
	return ll[idx%(len(ll)-1)]


def reduce(pc:str) -> str:
	return pc.replace('				',' ').replace('				',' ').replace('[		',' ').replace('[		',' ').replace('	',' ').replace('	',' ').replace('  ',' ').replace('  ',' ')


def split_pharagraf_on_sentences(lc_source:str) -> list:
	lc_str = lc_source.replace('. . .','...').replace('. .','..').replace('.',f'.{chr(2)}').replace('!',f'!{chr(2)}').replace('?',f'?{chr(2)}')
	ll = lc_str.split(chr(2))
	#print(f'll:{ll}')
	lll = [] # list of lengths of pharagraphs sentences
	min_len=0 # minimal sentence length, that will merged with the left neighbors
	for sent in ll:
		lll.append(len(sent))
		#print(f'{min_len} + {len(sent)}/{(len(ll)+1)} => {len(sent)/(len(ll)+1)}')
		min_len = min_len + len(sent)/(len(ll)+1)
	min_len = int(min_len)+1
	min_len = 6
	#print(f'lll: {lll}')
	#print(f'min_len: {min_len}')
	ll_merged_to_left = [] # list of sentences that needs to be merged with its left neigborn
	for i in range(len(lll)):
		if lll[i]<min_len:
			ll_merged_to_left.append(i)
	ll_new_list = []
	ln_counter = 0
	for element in ll:
		if ln_counter == 0:
			ll_new_list.append(element)
		if ln_counter>0   and	not ln_counter in ll_merged_to_left:
			ll_new_list.append(element)
		if ln_counter>0   and   ln_counter in ll_merged_to_left:
			ll_new_list[len(ll_new_list)-1] = ll_new_list[len(ll_new_list)-1] + (' ' if element not in [',','.','!','?','-','"',"'",' '] else '') + element.strip()
			ll_new_list[len(ll_new_list)-1] = reduce(ll_new_list[len(ll_new_list)-1].strip())
		ln_counter += 1
	return ll_new_list







class oFile():
	def __init__(self,name,size):
		self.name = name
		self.size = str(size) +' b'
		if size >1024:
			self.size = str(round(size / 1024)) + ' Kb'
		if size > 1048576:
			self.size = str(round(size / 1048576)) + ' Mb'
		if size > 1073741824:
			self.size = str(round(size / 1073741824)) + ' Gb'