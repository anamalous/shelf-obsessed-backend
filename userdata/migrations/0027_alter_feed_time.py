# Generated by Django 4.2.2 on 2023-10-31 17:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0026_alter_feed_time_alter_reports_repmonth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(22, 32, 0, 373045)),
        ),
    ]
