# Generated by Django 3.2.10 on 2021-12-22 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syllable',
            name='id',
        ),
        migrations.AddField(
            model_name='syllable',
            name='ready',
            field=models.IntegerField(default=0, null=True, verbose_name='Признак выученности'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='examples',
            field=models.TextField(default='', null=True, verbose_name='Примеры'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='show_count',
            field=models.IntegerField(default=0, null=True, verbose_name='Количество показов'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='transcription',
            field=models.TextField(default='', null=True, verbose_name='Транскрипция'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='translations',
            field=models.TextField(default='', null=True, verbose_name='Переводы'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='word',
            field=models.TextField(default='', primary_key=True, serialize=False, unique=True, verbose_name='Слово'),
        ),
    ]
