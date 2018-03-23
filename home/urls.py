from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),

    url(r'^organizations', views.OrganizationView, name='organizations'),
    url(r'^newOrganization.html$',views.newOrganizationView,name='newOrganization'),
    url(r'^submitNewOrganization$',views.submitNewOrganization,name='submitNewOrganization'),
]
