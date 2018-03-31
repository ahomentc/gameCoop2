from django.conf.urls import url
from . import views

app_name = 'org_work'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/projects$', views.IndexView, name='index'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/projects/(?P<project_id>\d+)/$', views.IndividualProjectView, name='individualProject'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/$', views.ProjectView, name='projects'),

    # create new project

    # url(r'^(?P<organization_id>\d+)/newCategory.html$',views.newCategoryView,name='newCategory'),
    # url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newCategory.html$',views.newCategoryView,name='newSubCategory'),
    # url(r'^(?P<organization_id>\d+)/submitNewCategory$',views.submitNewCategory,name='submitNewCategory'),
    # url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitNewCategory$',views.submitNewCategory,name='submitNewSubCategory'),
]
