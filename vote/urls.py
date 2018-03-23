from django.conf.urls import url
from . import views

app_name = 'vote'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/$', views.IndexView, name='index'),   #http://127.0.0.1:8000/vote/categories/2
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<question_id>\d+)\/$', views.DetailView, name='detail'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<question_id>\d+)\/results$', views.ResultsView, name='results'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<question_id>\d+)\/vote$', views.vote, name='vote'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newPoll.html$',views.newPollView, name='newPoll'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitNewPoll$', views.submitNewPoll, name='submitNewPoll'),
]
