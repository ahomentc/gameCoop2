from django.conf.urls import url
from . import views
from . import GitIntegration

app_name = 'org_work'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/categoryWork', views.IndexView, name='index'),
    url(r'^(?P<organization_id>\d+)/projects/(?P<project_id>\d+)/$', views.IndividualProjectView, name='individualProjectNoCat'),
    url(r'^(?P<organization_id>\d+)/projects/(?P<project_id>\d+)/(?P<category_id>\d+)/$', views.IndividualProjectView, name='individualProject'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/$', views.ProjectView, name='projects'),

    # create new project
    url(r'^(?P<organization_id>\d+)/newProject.html$',views.newProjectView,name='newProject'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newProject.html$',views.newProjectView,name='newSubProject'),
    url(r'^(?P<organization_id>\d+)/submitNewProject',views.submitNewProject,name='submitNewProject'),
    url(r'^(?P<organization_id>\d+)/(?P<original_cat>\d+)/submitNewProject$',views.submitNewProject,name='submitNewSubProject'),

    # submit work
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/SubmitWorkView', views.SubmitWorkView, name='SubmitWorkView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitWork', views.submitWork, name='submitWork'),

    # view non accepted contribution
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/pendingWork$', views.pendingWork, name='pendingWork'),

    # ajax
    url(r'(?P<organization_id>\d+)/(?P<project_id>\d+)/CreateGitRepo',GitIntegration.CreateGitRepo,name='CreateGitRepo'),
    url(r'(?P<organization_id>\d+)/(?P<project_id>\d+)/ConnectGitHub',GitIntegration.ConnectGitHub,name='ConnectGitHub'),
    url(r'(?P<organization_id>\d+)/(?P<organization_name>[\w\s\S]+)/(?P<project_id>\d+)/(?P<project_name>[\w\s\S]+)/getGitURL',GitIntegration.getGitURL,name='getGitURL'),
    url(r'^ProjectsInCommon', views.ProjectsInCommon, name='ProjectsInCommon'),
    url(r'^contribVote',views.voteForContrib,name='voteForContrib'),
    url(r'^acceptRejectWork',views.acceptRejectWork,name='acceptRejectWork'),
]
