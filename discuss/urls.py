from django.conf.urls import url
from . import views

app_name = 'discuss'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newPost', views.newPostView, name='newPost'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitNewPost', views.submitNewPost, name='submitNewPost'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<post_id>\d+)/submitReply$', views.submitReply, name='submitReply'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<post_id>\d+)/(?P<parent_id>\d+)/submitReply$', views.submitReply, name='submitSubReply'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<post_id>\d+)/(?P<reply_id>\d+)/editReply', views.editReply, name='editReply'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<post_id>\d+)/(?P<reply_id>\d+)/deleteReply', views.deleteReply, name='deleteReply'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<post_id>\d+)/viewPost$', views.IndividualPost, name='IndividualPost'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/ideaDiscussion', views.IdeaDiscussion, name='IdeaDiscussion'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/votingDiscussion', views.VotingDiscussion, name='VotingDiscussion'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/generalDiscussion', views.Index, name='Index'),

    url(r'^replyVote',views.voteForReply,name='replyVote'),
    url(r'^postVote',views.voteForPost,name='postVote')
]
