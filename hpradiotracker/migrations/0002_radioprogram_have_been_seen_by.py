# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 19:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hpradiotracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='radioprogram',
            name='have_been_seen_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
