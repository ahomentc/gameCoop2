from django.conf.urls import url
from . import views

app_name = 'consensusEditing'

urlpatterns = [
    # view main text-doc
    url(r'^(?P<textdoc_id>\d+)/(?P<organization_id>\d+)/textDoc', views.textDoc,name='textDoc'),

    # edit main text-doc
    url(r'^(?P<textdoc_id>\d+)/(?P<organization_id>\d+)/editTextDoc', views.editTextDoc,name='editTextDoc'),

    # view the proposals
    url(r'^(?P<main_text_doc_id>\d+)/(?P<organization_id>\d+)/proposals', views.viewProposals, name='viewProposals'),

    # view specific proposal
    url(r'^(?P<text_proposal_id>\d+)/(?P<organization_id>\d+)/viewTextProposal', views.viewTextProposal,name='viewTextProposal'),

    # vote
    url(r'^proposalVote',views.proposalVote,name='proposalVote'),
]
