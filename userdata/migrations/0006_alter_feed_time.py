# Generated by Django 4.2.2 on 2023-09-24 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0005_alter_feed_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(22, 3, 38, 250792)),
        ),
    ]