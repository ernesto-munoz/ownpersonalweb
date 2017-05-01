# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.http import HttpResponse
from django.views import View
from django.template import loader


class CurriculumView(View):
    template_name = 'curriculum/curriculum.html'

    def get(self, request):
        template = loader.get_template(template_name=self.template_name)
        context = {}
        return HttpResponse(template.render(context, request))
