from django.conf.urls import url
from . import views

app_name = 'org_work'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/projects$', views.IndexView, name='index'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/projects$', views.IndexView, name='index'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/$', views.ProjectView, name='projects'),
]
