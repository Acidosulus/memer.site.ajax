# Generated by Django 3.2.10 on 2021-12-24 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocapp', '0002_auto_20211222_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='syllable',
            name='last_view',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата/Время последнего просмотра'),
        ),
    ]
