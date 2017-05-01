# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import RadioProgram, UserProgramDown

# Register your models here.
admin.site.register(RadioProgram)
admin.site.register(UserProgramDown)
