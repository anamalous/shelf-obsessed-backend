# Generated by Django 4.2.2 on 2023-09-25 18:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0020_reviews_isreply_alter_feed_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(0, 25, 31, 801186)),
        ),
    ]
