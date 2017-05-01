# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SentMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=50)),
                ('sent_date', models.DateTimeField(verbose_name='sent date')),
                ('sender_email', models.EmailField(max_length=254)),
                ('message_subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
    ]