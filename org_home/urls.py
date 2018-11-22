from django.conf.urls import url
from . import views

app_name = 'org_home'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/$', views.IndexView, name='index'),

    url(r'^(?P<organization_id>\d+)/categories$', views.CategoryView, name='categories'),

    # new category
    url(r'^(?P<organization_id>\d+)/newCategory.html$',views.newCategoryView,name='newCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newCategory.html$',views.newCategoryView,name='newSubCategory'),
    url(r'^(?P<organization_id>\d+)/submitNewCategory$',views.submitNewCategory,name='submitNewCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitNewCategory$',views.submitNewCategory,name='submitNewSubCategory'),

    # access to organization
    url(r'^(?P<organization_id>\d+)/joinOrganization$', views.JoinOrganization, name='joinOrganization'),
    url(r'^(?P<organization_id>\d+)/orgMembers$', views.orgMembersView, name='orgMembersView'),
    url(r'^(?P<organization_id>\d+)/pendingOrgMembers$', views.orgPendingMembersView, name='orgPendingMembersView'),
    url(r'^(?P<organization_id>\d+)/(?P<pending_member_id>\d+)/grantOrgAccess$', views.GrantAccessToOrg, name='GrantOrgAccess'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/$', views.IndividualCategoryView, name='individualCategory'),

    # access to category
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/joinCategory$', views.JoinCategory, name='joinCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/members$', views.membersView, name='membersView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/moderators', views.modsView, name='modsView'),
    url(r'^makeMod', views.makeMod, name='makeMod'),

    # viewing and accepting pending members of category
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/pendingMembers$', views.pendingMembersView, name='pendingMembersView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<pending_member_id>\d+)/grant_access$', views.GrantAccess, name='GrantAccess'),

    # positions
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/positions', views.positionsView, name='positionsView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newPositionView', views.newPositionView, name='newPositionView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitNewPosition$', views.submitNewPosition,name='submitNewPosition'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<position_id>\d+)/$', views.individualPosition, name='individualPosition'),

    # request to join position
    url(r'^requestToJoinPos', views.requestToJoinPos, name='requestToJoinPos'),
    url(r'^grantAccessToPosition', views.grantAccessToPosition, name='grantAccessToPosition'),

    # helper
    url(r'^userInCategory',views.userInCategory,name='userInCategory'),
]
