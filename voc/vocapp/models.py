from django.db import models

# Create your models here.
class Syllable(models.Model):
	rowid = models.BigAutoField(primary_key=True)
	word = models.TextField( verbose_name = 'Слово', default = '', unique = True)
	userid = models.IntegerField(null=True, verbose_name = 'Идентификатор пользователя', default = 0)
	transcription = models.TextField(null=True, verbose_name = 'Транскрипция', default = '', blank=True)
	translations = models.TextField(null=True, verbose_name = 'Переводы', default = '', blank=True)
	examples = models.TextField(null=True, verbose_name = 'Примеры', default = '', blank=True)
	show_count =models.IntegerField(null=True, verbose_name = 'Количество показов', default = 0)
	ready = models.IntegerField(null=True, verbose_name = 'Признак выученности', default = 0)
	last_view = models.DateTimeField(null=True, verbose_name='Дата/Время последнего просмотра', auto_now_add = True)

class Words(models.Model):
	rowid = models.BigAutoField(primary_key=True)
	word = models.TextField( verbose_name = 'Слово', default = '', unique = True)
	transcription = models.TextField(null=True, verbose_name = 'Транскрипция', default = '', blank=True)
	translations = models.TextField(null=True, verbose_name = 'Переводы', default = '', blank=True)
	examples = models.TextField(null=True, verbose_name = 'Примеры', default = '', blank=True)
	ready = models.IntegerField(null=True, verbose_name = 'Обработано', default = 0)
	dt = models.DateTimeField(null=True, verbose_name='Дата/Время скачанности', auto_now_add = True)
	notfound = models.IntegerField(null=True, verbose_name = 'Признак не найденности на сайте', default = 0)
	parent_word = models.TextField(null=True, verbose_name = 'Исходная форма слова', default = '', blank=True)

class Books(models.Model):
	id_book = models.AutoField(primary_key=True)
	userid = models.IntegerField(null=True, verbose_name = 'Идентификатор пользователя', default = 0)
	book_name = models.TextField(null=True, verbose_name = 'Название книги', default = '', blank=True)
	current_paragraph = models.IntegerField(null=True, verbose_name='Текущий читаемый параграф', default=1)
	dt = models.DateTimeField(null=True, verbose_name='Дата/Время последнего обращения к книге', auto_now_add = True)

class Paragraphs(models.Model):
	id_paragraph = models.AutoField(primary_key=True)
	userid = models.IntegerField(null=True, verbose_name = 'Идентификатор пользователя', default = 0)
	id_book = models.IntegerField(null=True, verbose_name = 'Идентификатор книги', default = 0, blank=True)
	paragraph = models.TextField(null=True, verbose_name = 'Параграф книги', default = '', blank=True)

class Phrases(models.Model):
	id_phrase = models.AutoField(primary_key=True)
	userid = models.IntegerField(null=True, verbose_name = 'Идентификатор пользователя', default = 0)
	phrase = models.TextField(null=True, verbose_name = 'Фраза', default = '', blank=True)
	translation = models.TextField(null=True, verbose_name = 'Перевод', default = '', blank=True)
	show_count =models.IntegerField(null=True, verbose_name = 'Количество показов', default = 0)
	ready = models.IntegerField(null=True, verbose_name = 'Признак выученности', default = 0)
	last_view = models.DateTimeField(null=True, verbose_name='Дата/Время последнего просмотра', auto_now_add = True)
	dt = models.DateTimeField(null=True, verbose_name='Дата/Время последнего обращения к книге', auto_now_add = True)


