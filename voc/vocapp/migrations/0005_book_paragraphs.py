# Generated by Django 3.2.10 on 2022-01-11 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocapp', '0004_auto_20211225_0221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id_book', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.TextField(blank=True, default='', null=True, verbose_name='Название книги')),
                ('current_paragraph', models.IntegerField(default=1, null=True, verbose_name='Текущий читаемый параграф')),
            ],
        ),
        migrations.CreateModel(
            name='Paragraphs',
            fields=[
                ('id_paragraph', models.AutoField(primary_key=True, serialize=False)),
                ('paragraph', models.TextField(blank=True, default='', null=True, verbose_name='Параграф книги')),
            ],
        ),
    ]
