# Generated by Django 4.2.2 on 2023-09-24 17:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0014_delete_allbooks_delete_booklist_alter_feed_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covers',
            name='cfile',
            field=models.ImageField(default='def.jpg', max_length=200, null=True, upload_to='media'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='time',
            field=models.TimeField(default=datetime.time(23, 5, 42, 511283)),
        ),
    ]
