# Generated by Django 4.2.2 on 2023-09-25 14:58

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0018_remove_reviews_replyto_reviews_replies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(20, 28, 18, 466303)),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='replies',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), null=True, size=None),
        ),
    ]
