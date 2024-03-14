# Generated by Django 4.2.2 on 2023-09-26 03:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0021_alter_feed_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='isreply',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='replies',
        ),
        migrations.AddField(
            model_name='reviews',
            name='replyto',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(8, 31, 48, 740397)),
        ),
    ]