# Generated by Django 4.2.2 on 2023-09-24 16:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0009_alter_feed_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='summary',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(22, 16, 51, 714395)),
        ),
    ]