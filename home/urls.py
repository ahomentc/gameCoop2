from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    # url(r'^$', views.IndexView, name='index'),
    url(r'^$', views.OrganizationView, name='index'),

    url(r'^organizations', views.OrganizationView, name='organizations'),
    url(r'^newOrganization.html$',views.newOrganizationView,name='newOrganization'),
    url(r'^submitNewOrganization$',views.submitNewOrganization,name='submitNewOrganization'),
    url(r'^submitNewPotentialOrg$',views.submitNewPotentialOrg,name='submitNewPotentialOrg'),

    url(r'^(?P<organization_id>\d+)/orgTypeView',views.orgTypeView,name='orgTypeView'),
    url(r'^(?P<organization_id>\d+)/submitOrgType', views.submitOrgType, name='submitOrgType'),

    url(r'^(?P<organization_id>\d+)/setMonetaryDistView', views.setMonetaryDistView, name='setMonetaryDistView'),
    url(r'^(?P<organization_id>\d+)/submitMonetaryDist', views.submitMonetaryDist, name='submitMonetaryDist'),

    url(r'^(?P<organization_id>\d+)/setGovernanceView', views.setGovernanceView, name='setGovernanceView'),
]
