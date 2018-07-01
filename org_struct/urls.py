from django.conf.urls import url
from . import views

app_name = 'org_struct'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/$', views.IndexView, name='index'),

    # url(r'^(?P<organization_id>\d+)/monetary_distribution$', views.MoneyDistributionView,name='monetary_distribution'),
    # url(r'^(?P<organization_id>\d+)/community_editing', views.community_editing,name='community_editing')
]
