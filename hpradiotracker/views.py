# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json

from django.conf import settings

from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from models import RadioProgram, UserProgramDown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils import TrackerUtils


# Signup, login and logout

class SignUpView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'hpradiotracker/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/hpradiotracker')

        return render(request, 'hpradiotracker/signup.html', {'form': form})


class LoginView(View):

    def post(self, request):
        username = request.POST['login-username']
        password = request.POST['login-password']

        result_dict = {
            'valid_login': True,
            'message': None
        }

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                result_dict['valid_login'] = True
                result_dict['message'] = 'Success Login'
            else:
                result_dict['valid_login'] = False
                result_dict['message'] = 'Disabled account'
        else:
            result_dict['valid_login'] = False
            result_dict['message'] = 'Invalid Login'

        return HttpResponse(json.dumps(result_dict), content_type='application/json')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/hpradiotracker')
        # return HttpResponse('Success Logout')

# Services


class UpdateRadioDatabaseView(View):
    def post(self, request):
        print 'Update Radio Database View (Begin)'
        how_many_pages = int(request.POST['how_many_pages'])
        radio_programs_list = TrackerUtils().get_radio_programs_data(how_many_pages=how_many_pages)
        for radio_program in radio_programs_list:
            new_radio_program = RadioProgram()
            new_radio_program.inner_identifier = radio_program[0]
            new_radio_program.program_name = radio_program[1]
            new_radio_program.added_date = radio_program[2]

            # check if the inner identifier already exists
            if not RadioProgram.objects.filter(inner_identifier=new_radio_program.inner_identifier).exists():
                new_radio_program.save()

        print 'Update Radio Database View (End)'
        return HttpResponse('Updated')


class TrackerMainView(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        query_string = request.GET.get('query_string', '')

        # create payload for the template
        payload = {
            'db_radio_programs_list': RadioTableUtilities().get_radio_programs_list(query_string=query_string, page=page),
            # if the user is authenticated, the inner_identifier of the program that has downloaded
            'user_program_id': RadioTableUtilities().get_downloaded_for_user(user=request.user),
            'query_string': query_string
        }

        return render(request, 'hpradiotracker/index.html', payload)


class ChangeSeenView(View):

    def post(self, request):
        identifier = request.POST['inner_identifier']
        radio_program = RadioProgram.objects.all().filter(inner_identifier=identifier)
        result_dict = {
            'new_image_url': None
        }

        if len(radio_program) >= 1:
            if request.user in radio_program[0].have_been_seen_by.all():
                result_dict['new_image_url'] = '/static/hpradiotracker/img/iconmonstr-eye-10-240_not_seen.png'
                radio_program[0].have_been_seen_by.remove(request.user)
            else:
                result_dict['new_image_url'] = '/static/hpradiotracker/img/iconmonstr-eye-1-240_seen.png'
                radio_program[0].have_been_seen_by.add(request.user)

        return HttpResponse(json.dumps(result_dict), content_type='application/json')


class DownloadFileView(View):

    def post(self, request):
        result_dict = {
            'message': None
        }

        identifier = request.POST['inner_identifier']
        username = request.user.username
        radio_programs = RadioProgram.objects.all().filter(inner_identifier=identifier)

        # already downloaded
        user_program_down_list = UserProgramDown.objects.all().filter(radio_program_id=radio_programs[0], user_id=request.user)
        if len(user_program_down_list) > 0:
            print "File already downloaded!"
            result_dict['message'] = 'File already downloaded!'
            return HttpResponse(json.dumps(result_dict), content_type='application/json')

        # check if the user has any program already downloaded
        user_program_down_list = UserProgramDown.objects.all().filter(user_id=request.user)
        for user_program_down in user_program_down_list:
            print "Old downloaded(deleted): " + user_program_down.radio_program_id.inner_identifier + " " + username
            os.remove('{}\\hpradiotracker\\static\\hpradiotracker\\media\\{}_{}.mp3'.format(os.getcwd(),
                                                                                            user_program_down.radio_program_id.inner_identifier,
                                                                                            username))
            os.remove('{}\\hpradiotracker\\static\\hpradiotracker\\media\\{}_{}.torrent'.format(os.getcwd(),
                                                                                                user_program_down.radio_program_id.inner_identifier,
                                                                                                username))
            user_program_down.delete()

        # save the new downloaded program
        new_user_program_down = UserProgramDown(radio_program_id=radio_programs[0], user_id=request.user)
        new_user_program_down.save()

        # download the program
        TrackerUtils().download_torrent(inner_identifier=identifier, username=request.user.username)

        result_dict['message'] = 'Download finished!'

        return HttpResponse(json.dumps(result_dict), content_type='application/json')


class GetPlayFileUrlView(View):

    def post(self, request):
        if request.user.is_authenticated:
            result_dict = {
                'audio_url': None
            }
            user_program_down = UserProgramDown.objects.all().filter(user_id=request.user)
            if len(user_program_down) > 0:
                inner_identifier = user_program_down[0].radio_program_id.inner_identifier
                local_filename = os.path.normpath(
                    '\\static\\hpradiotracker\\media\\{}_{}.mp3'.format(inner_identifier,
                                                                                        request.user.username)
                )
                result_dict['audio_url'] = local_filename

            return HttpResponse(json.dumps(result_dict), content_type='application/json')


class GetRadioTableHtml(View):

    def post(self, request):
        page = request.POST.get('page', 1)
        query_string = request.POST.get('query_string', '')

        context = {
            'db_radio_programs_list': RadioTableUtilities().get_radio_programs_list(query_string=query_string,
                                                                                    page=page),
            'user_program_id': RadioTableUtilities().get_downloaded_for_user(user=request.user),
            'query_string': query_string
        }

        rendered = loader.render_to_string(template_name='hpradiotracker/table.html', context=context, request=request)

        result_dict = {
            'rendered': rendered
        }
        return HttpResponse(json.dumps(result_dict), content_type='application/json')

# Utilities


class RadioTableUtilities:
    items_by_page = 10

    def __init__(self):
        pass

    def get_radio_programs_list(self, query_string, page):
        if query_string == '':
            radio_program_list = RadioProgram.objects.all().filter().reverse()
        else:
            radio_program_list = RadioProgram.objects.all().filter(program_name__icontains=query_string).reverse()
        paginator = Paginator(radio_program_list, self.items_by_page)
        try:
            radio_programs = paginator.page(page)
        except PageNotAnInteger:
            radio_programs = paginator.page(1)
        except EmptyPage:
            radio_programs = paginator.page(paginator.num_pages)

        return radio_programs

    def get_downloaded_for_user(self, user):
        if user.is_authenticated:
            user_program_down_list = UserProgramDown.objects.all().filter(user_id=user)
            if len(user_program_down_list) > 0:
                return  user_program_down_list[0].radio_program_id.inner_identifier
        return None


