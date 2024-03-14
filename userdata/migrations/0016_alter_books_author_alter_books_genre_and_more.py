# Generated by Django 4.2.2 on 2023-09-24 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0015_alter_covers_cfile_alter_feed_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='books',
            name='genre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='books',
            name='year',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(23, 13, 13, 777922)),
        ),
    ]