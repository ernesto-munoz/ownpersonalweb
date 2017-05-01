# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.db import models


class RadioProgram(models.Model):
    inner_identifier = models.CharField(max_length=6, unique=True, default='inner_identifier')
    program_name = models.CharField(max_length=200, default='name')
    added_date = models.CharField(max_length=15, default='added_date')

    have_been_seen_by = models.ManyToManyField(User)

    def __unicode__(self):
        return '{} {} {}'.format(
            self.program_name,
            self.inner_identifier,
            self.added_date
        )

    class Meta:
        ordering = ('inner_identifier', 'program_name', 'added_date')


class UserProgramDown(models.Model):
    radio_program_id = models.ForeignKey(RadioProgram)
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        return '{} {}'.format(
            self.radio_program_id,
            self.user_id
        )

    class Meta:
        ordering = ('radio_program_id', 'user_id')
