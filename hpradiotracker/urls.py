from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from views import UpdateRadioDatabaseView, TrackerMainView, \
    SignUpView, LoginView, LogoutView, ChangeSeenView, DownloadFileView, GetPlayFileUrlView, GetRadioTableHtml

app_name = 'hpradiotracker'
urlpatterns = [
    url(r'^$', TrackerMainView.as_view(), name='tracker-main-view'),

    url(r'^signup/$', SignUpView.as_view(), name='sign-up-view'),
    url(r'^login$', LoginView.as_view(), name='login-view'),
    url(r'^logout$', LogoutView.as_view(), name='logout-view'),

    url(r'^update_radio_database$', UpdateRadioDatabaseView.as_view(), name='update-radio-database-view'),
    url(r'^change_seen$', ChangeSeenView.as_view(), name='change-seen'),
    url(r'^download_file$', DownloadFileView.as_view(), name='download-file-view'),
    url(r'^get_play_file_url$', GetPlayFileUrlView.as_view(), name='get-play-file-url'),
    url(r'^get_radio_table_html$', GetRadioTableHtml.as_view(), name='get-radio-table-html')


]