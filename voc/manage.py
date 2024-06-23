#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
def main():
	"""Run administrative tasks."""
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voc.settings')
	db_ready = False
	while not db_ready:
		try:
			from django.core.management import execute_from_command_line
			from django.db import connection
			cursor = connection.cursor()
			cursor.execute("SELECT 1")
			try:
				response = requests.get(f"{settings.API_ADRESS}/GetAllUsers/{settings.SECRET_KEY}/")
				db_ready = True
			except:
				# Обработка случаев, когда база данных недоступна
				print("API server unreachable...")
				import time
				time.sleep(5)  # Подождите 5 секунд перед повторной попыткой
		except:
			# Обработка случаев, когда база данных недоступна
			print("Database unreachable....")
			import time
			time.sleep(5)  # Подождите 5 секунд перед повторной попыткой
	execute_from_command_line(sys.argv)


if __name__ == '__main__':
	main()
