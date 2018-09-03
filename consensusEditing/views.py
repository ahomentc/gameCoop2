from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
import os
import itertools

from django.shortcuts import render
from home.models import Organizations
from org_home.models import Categories
from django.db.models import F
from consensusEditing.models import TextDoc,vote
from django.views.decorators.csrf import csrf_exempt
from activity_feed.views import submitActivity

@login_required
def textDoc(request, textdoc_id, organization_id=None):

    # get the text-doc from the id
    text_doc = get_object_or_404(TextDoc,id=textdoc_id)
    path = text_doc.pathToFile
    title = text_doc.title

    # get the text file
    with open(path, 'r') as f:
        text = f.read()

    organization = text_doc.organization

    return render(request, 'consensusEditing/text_doc.html',{'organization':organization,
                                                             'categories_list': Categories.objects.filter(organization=organization, ),
                                                             'text':text,
                                                             'textdoc_id':textdoc_id,
                                                             'title':title,
                                                             })

def editTextDoc(request, textdoc_id, organization_id=None):
    text = request.POST['content']

    text_doc = get_object_or_404(TextDoc, id=textdoc_id)
    path = text_doc.pathToFile
    title = text_doc.title

    organization = text_doc.organization

    # get the main document
    if(text_doc.isMain == True):
        mainDoc = text_doc
    else:
        mainDoc = text_doc.mainDoc

    # delete any old proposals a user has for the same main document
    if len(TextDoc.objects.filter(mainDoc=mainDoc,poster=request.user)) > 0:
        TextDoc.objects.filter(mainDoc=mainDoc, poster=request.user).delete()
        #deleteTextDoc()

    # create the new proposal
    proposal_text_doc = TextDoc.objects.create(title=title,
                                      description=text_doc.description,
                                      location_type=text_doc.location_type,
                                      isMain=False,
                                      mainDoc=mainDoc,
                                      organization=organization,
                                      poster=request.user,
                                      )
    proposal_text_doc.save()
    proposal_path = "/Users/andrei/gameCoop2/storage/organizations/" + organization_id + "/proposals/" + \
                    str(mainDoc.pk) + "/" + str(proposal_text_doc.pk) + ".txt"
    proposal_text_doc.pathToFile = proposal_path
    proposal_text_doc.save()

    # create a vote object for that proposal
    voteObj = vote.objects.create(textDoc=proposal_text_doc)
    voteObj.save()

    # submit an activity
    url = reverse('consensusEditing:viewTextProposal', args=(proposal_text_doc.id,organization.id))
    submitActivity(str(request.user) + " proposed an edit to " + str(text_doc.title), url, organization_id)


    # in the proposals folder create a folder with the id of the main text doc and put the proposal doc in there
    if(text_doc.mainDoc == None):
        command = "cd storage " \
                  "\n cd organizations" \
                  "\n cd " + organization_id + \
                  "\n cd proposals" \
                  "\n mkdir " + str(text_doc.pk) + \
                  "\n cd " + str(text_doc.pk) + \
                  '\n echo "' \
                  + text + '" >> ' + str(proposal_text_doc.pk) + '.txt '

    else:
        command = "cd storage " \
                  "\n cd organizations" \
                  "\n cd " + organization_id + \
                  "\n cd proposals" \
                  "\n mkdir " + str(text_doc.mainDoc.pk) + \
                  "\n cd " + str(text_doc.mainDoc.pk) + \
                  '\n echo "' \
                  + text + '" >> ' + str(proposal_text_doc.pk) + '.txt '
    os.system(command)
    return render(request, 'consensusEditing/text_proposal.html', {'organization': organization,
                                                               'categories_list': Categories.objects.filter(organization=organization, ),
                                                              'text': text,
                                                              'highLighted_text':text,
                                                              'textdoc_id':proposal_text_doc.id,
                                                              'main_id': mainDoc.pk,
                                                              'title':title,
                                                              })

    # else:
    #     warning = "Updating the proposal will reset the voting and discussion. Do you wish to continue?"
    #     return render(request, 'consensusEditing/text_doc.html', {'organization': organization,
    #                                                               'text': text,
    #                                                               'textdoc_id': textdoc_id,
    #                                                               'title': title,
    #                                                               'error': warning
    #                                                               })

def viewProposals(request,main_text_doc_id,organization_id=None):
    main_text_doc = get_object_or_404(TextDoc, id=main_text_doc_id)
    organization = main_text_doc.organization
    proposalsList = TextDoc.objects.filter(mainDoc=main_text_doc,)
    return render(request, 'consensusEditing/proposals.html', {'organization': organization,
                                                               'categories_list': Categories.objects.filter(organization=organization, ),
                                                               'proposals_list': proposalsList
    })


def viewTextProposal(request, text_proposal_id, organization_id=None):
    organization = None

    # get the text-doc from the id
    text_doc = get_object_or_404(TextDoc,id=text_proposal_id)
    path = text_doc.pathToFile
    title = text_doc.title

    organization = text_doc.organization

    # get the text file of the proposal
    with open(path, 'r') as f:
        text = f.read()

    # get the text of of the main doc
    main_doc = text_doc.mainDoc
    main_doc_path = main_doc.pathToFile
    with open(main_doc_path,'r') as f:
        main_text = f.read()

    # get the lines with the difference between the main and proposal
    linesWithDiff = getModifications(main_text,text)

    # highlight text on the modified lines
    highLighted_text = highlightText(linesWithDiff,text)

    return render(request, 'consensusEditing/text_proposal.html',{'organization':organization,
                                                             'categories_list': Categories.objects.filter(organization=organization, ),
                                                             'text':text,
                                                             'highLighted_text':highLighted_text,
                                                             'textdoc_id':text_proposal_id,
                                                             'title':title,
                                                             })

# returns a list of the line numbers that are different
def getModifications(original, modified):
    originalLines = original.split('\n')
    modifiedLines = modified.split('\n')

    linesWithDiff = []

    for i,(originalLine, modifiedLine) in enumerate(itertools.zip_longest(originalLines,modifiedLines)):
        if(originalLine!=modifiedLine):
            linesWithDiff.append(i)

    return linesWithDiff

# returns the text with highlighted html on the line numbers given
def highlightText(linesWithDiff,text):
    newText = ''
    lines = text.split('\n')
    for i,line in enumerate(lines):
        if(i in linesWithDiff):
            newLine = '<mark>' + line + '</mark>\n'
            newText += newLine
        else:
            newText += line
        newText += '\n'
    return newText

@csrf_exempt
def proposalVote(request):
    text_proposal_id = int(request.POST.get('text_proposal_id'))

    # get the text-doc from the id
    proposal = get_object_or_404(TextDoc, id=text_proposal_id)
    proposal_path = proposal.pathToFile

    # get the text file of the proposals
    with open(proposal_path, 'r') as f:
        proposal_text = f.read()

    # get the text of of the main doc
    main_doc = proposal.mainDoc
    main_doc_path = main_doc.pathToFile

    voteObj = vote.objects.filter(textDoc=proposal)[0]

    votes = voteObj.votes
    voters = voteObj.voters.all()
    voteObj.save()

    threshhold = getPassingThreshhold(text_proposal_id)

    if request.user not in voters:
        voteObj.voters.add(request.user)
        voteObj.votes = F('votes') + 1
        voteObj.save()

    # if yes votes passes the threshold then overwrite main with the proposal
    if votes >= threshhold:
        with open(main_doc_path,'w') as f:
            f.write(proposal_text)

        # commit the main git with the new edit
        commitTextDocGit(main_doc.pk)

        # delete the proposal
        deleteTextDoc(proposal.pk)

    return HttpResponse(status=204)

def getPassingThreshhold(text_proposal_id):
    proposal = get_object_or_404(TextDoc, id=text_proposal_id)
    threshhold = 0;

    # maybe put the threshold in the model of the organization
    if proposal.location_type == 'Organization':
        organization = proposal.organization
        numUsers = organization.members.count()
        threshhold = int(numUsers * .51)

    return threshhold


def deleteTextDoc(text_doc_id):
    text_doc = get_object_or_404(TextDoc, id=text_doc_id)
    organization = text_doc.organization

    # remove from the file system
    if(text_doc.isMain):
        command = "cd storage " \
                  "\n cd organizations" \
                  "\n cd " + str(organization.pk) + \
                  "\n cd mains" \
                  "\n cd git" \
                  "\n rm -r " + str(text_doc.pk)
    else:
        command = "cd storage " \
                  "\n cd organizations" \
                  "\n cd " + str(organization.pk) + \
                  "\n cd proposals" \
                  "\n cd " + str(text_doc.mainDoc.pk) + \
                  "\n rm -r " + str(text_doc.pk) + ".txt"

    os.system(command)

    # remove from the database
    text_doc.delete()

def commitTextDocGit(text_doc_id):
    text_doc = get_object_or_404(TextDoc, id=text_doc_id)
    organization = text_doc.organization

    print("goes to git")

    command = "cd storage " \
              "\n cd organizations" \
              "\n cd " + str(organization.pk) + \
              "\n cd mains" \
              "\n cd git" \
              "\n git status" \
              "\n git add " + str(text_doc.pk) + ".txt" \
              "\n git commit " + str(text_doc.pk) + ".txt -m \"Updated " + str(text_doc.pk) + "\""

    os.system(command)
