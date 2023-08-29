import django
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from models import Books,Paragraphs

DJANGO_SETTINGS_MODULE="vocapp.settings"

pc_file_path = r'C:\voc\voc\Blood_of_the_Fold_by_Terry_Goodkind_Goodkind,_Terry_z_lib_org.txt'

lc_book_name = 'Blood of the Fold by Terry Goodkind'

ll_book = open (pc_file_path, "r", encoding='utf8').readlines()
for lc_paragraph in ll_book:
	lc_paragraph = lc_paragraph.replace(chr(13),'').replace(chr(10),'').replace(chr(12),'')
	#print(lc_paragraph)



print(lc_book)