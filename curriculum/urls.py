from django.conf.urls import url
from curriculum.views import CurriculumView

app_name = 'curriculum'
urlpatterns = [
    url(r'^$', CurriculumView.as_view(), name='curriculum')
]