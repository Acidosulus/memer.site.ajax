# Generated by Django 3.2.10 on 2022-01-11 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocapp', '0005_book_paragraphs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Book',
            new_name='Books',
        ),
    ]
