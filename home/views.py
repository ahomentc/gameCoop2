# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
import os
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from consensusEditing.views import commitTextDocGit

from .models import Organizations
from .models import MonetaryDistribution
from org_home.models import Categories
from consensusEditing.models import TextDoc

@login_required
def IndexView(request):
    return render(request, 'home/index.html',{'member_organizations_list': Organizations.objects.filter(
        members__id=request.user.id),
    })

@login_required
def OrganizationView(request):
    return render(request,'home/organizations.html',{'organizations_list':Organizations.objects.all()})

@login_required
def newOrganizationView(request):
    return render(request, 'home/newOrganization.html')

@login_required
def orgTypeView(request,organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    return render(request, 'home/orgType.html',{'organization':organization})

@login_required
def setMonetaryDistView(request, organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    return render(request, 'home/setMonetaryDistribution.html', {'organization': organization})

@login_required
def setGovernanceView(request, organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    return render(request, 'home/setGovernance.html', {'organization': organization})

@login_required
def submitNewPotentialOrg(request):
    if 'new_organization' in request.POST and request.POST['new_organization'] != '':
        # get the organization name
        organizationName = request.POST['new_organization']

        # first word in organization name uppercased
        formatedOrganizationName = ' '.join(word[0].upper() + word[1:] for word in organizationName.split())

        # returns error if the organization name already exists
        if Organizations.objects.filter(organization_name=formatedOrganizationName).exists():
            return render(request, 'home/newOrganization.html',
                          {'error_message': formatedOrganizationName + " already exists.", })

        # get the description
        description = request.POST['new_organization_desc']

        # create the organization, add the creator to the members list, and make the creator a moderator
        organization = Organizations.objects.create(organization_name=formatedOrganizationName,description=description)
        organization.members.add(request.user)
        organization.moderators.add(request.user)

        return HttpResponseRedirect(reverse('home:orgTypeView', args=(organization.id,)))

    else:
        return render(request, 'home/newOrganization.html', {
            'error_message': "Please enter a organization.",
        })

@login_required
def submitOrgType(request,organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)

    if 'org_type' in request.POST:
        organization.organization_type = request.POST['org_type']
        return HttpResponseRedirect(reverse('home:setMonetaryDistView', args=(organization.id,)))
    else:
        return render(request, 'home/orgType.html', {'organization': organization,
                                                     'error_message':'Please select a type of organization'})


@login_required
def submitMonetaryDist(request, organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)

    monetaryDist = MonetaryDistribution.objects.create(organization=organization)

    if 'iwfPercent' in request.POST:
        monetaryDist.InvestorsWorkersFounders = request.POST['iwfPercent']

    if 'orgBankPercent' in request.POST:
        monetaryDist.OrgBank = request.POST['orgBankPercent']

    if 'sharesPerDollar' in request.POST:
        monetaryDist.sharesPerDollarInvested = request.POST['sharesPerDollar']

    if 'sharesPerForumUpvote' in request.POST:
        monetaryDist.sharesPerUpvoteOnForumPost = request.POST['sharesPerForumUpvote']

    if 'sharesPerContribUpvote' in request.POST:
        monetaryDist.sharesPerUpvoteOnContribution = request.POST['sharesPerContribUpvote']

    if 'sharesPerAcceptedIdea' in request.POST:
        monetaryDist.sharesPerAcceptedPostedIdea = request.POST['sharesPerAcceptedIdea']

    if 'baseNumberSharesUsedContrib' in request.POST:
        monetaryDist.sharesPerUsedContrib = request.POST['baseNumberSharesUsedContrib']

    if 'initialFounderNum' in request.POST:
        monetaryDist.numOriginalFounders = request.POST['initialFounderNum']

    if 'initialFounderBonus' in request.POST:
        monetaryDist.sharesPerFounderBonus = request.POST['initialFounderBonus']

    if 'codeUseReward' in request.POST:
        monetaryDist.sharesPerEachUseOfCode = request.POST['codeUseReward']

    if 'SharesPerLine' in request.POST:
        monetaryDist.sharesPerLineAcceptedCode = request.POST['SharesPerLine']

    if 'machine_learning_distr' in request.POST:
        if request.POST['machine_learning_distr'] == 'true':
            monetaryDist.machineLearningShareDistr = True
        elif request.POST['machine_learning_distr'] == 'false':
            monetaryDist.machineLearningShareDistr = False

    monetaryDist.save()

    return HttpResponseRedirect(reverse('home:setGovernanceView', args=(organization.id,)))


# submit creation of a new organization
@login_required
def submitNewOrganization(request):
    if 'new_organization' in request.POST and request.POST['new_organization'] != '':
        closedOrganization = False
        gate_keeper = ''
        # close_organization is a checkbox of if people need persmission to join the category
        if 'closed_organization' in request.POST:
            closedOrganization = True
            # gate_keeper is who can let people join the community. It can either be anyone in the community
            # or the moderator. access is the name of the radio field
            gate_keeper = request.POST['access']

        organizationName =  request.POST['new_organization']
        # first word in organization name uppercased
        formatedOrganizationName = ' '.join(word[0].upper() + word[1:] for word in organizationName.split())

        # returns error if the organization name already exists
        if Organizations.objects.filter(organization_name=formatedOrganizationName).exists():
            return render(request, 'home/newOrganization.html', {'error_message': formatedOrganizationName + " already exists.",})

        # create the organization, add the creator to the members list, and make the creator a moderator
        organization = Organizations.objects.create(organization_name=formatedOrganizationName,closed_organization = closedOrganization,gateKeeper=gate_keeper)
        organization.members.add(request.user)
        organization.moderators.add(request.user)

        # auto create executive category
        category = Categories.objects.create(organization=organization,parent=None,category_name="Executive",closed_category = True, gateKeeper="moderators")
        category.members.add(request.user)
        category.moderators.add(request.user)

        # create file system for organization and git
        organization.save()
        CreateOrgFiles(organization.pk)
        CreateOrgBaseFiles(organization.pk)

        return HttpResponseRedirect(reverse('home:organizations'))
    else:
        return render(request, 'home/newOrganization.html', {
            'error_message': "Please enter a organization.",
        })

def CreateOrgFiles(organization_id):

    organization_id = str(organization_id)

    command = "cd storage " \
              "\n cd organizations" \
              "\n mkdir " + organization_id + \
              "\n cd " + organization_id + \
              "\n mkdir categories" \
              "\n mkdir projects" \
              "\n mkdir mains" \
              "\n mkdir proposals" \
              "\n cd mains" \
              "\n mkdir git" \
              "\n cd git" \
              "\n git init"

    os.system(command)

def CreateOrgBaseFiles(organization_id):

    organization = get_object_or_404(Organizations, pk=organization_id)
    organization_id = str(organization_id)


    # create the text-doc model
    text_doc = TextDoc.objects.create(title="Monetary Distribution",
                                                description="How money is distributed through organization",
                                                location_type="Organization",
                                                isMain=True,
                                                organization=organization,
                                                )

    text_doc.save()
    path = "/Users/andrei/gameCoop2/storage/organizations/" + organization_id + "/mains/git/" + str(text_doc.pk) + ".txt"
    text_doc.pathToFile = path
    text_doc.save()

    text = '\n echo "------------------------\nRevenue Money:\nBase Payment + benefits*\n* actually 0 for now' \
              '\nDevelopment Costs: Revenue - Base Payment\n100% development costs\nProfit: Revenue - Base Payment - Development Costs\n-------------------------' \
              '\n\nProfit Money:\n40%: Worker Payment*\n* Work payment Individually distributed by Percent = Individual Points / Total Points' \
              '\n\n30%: Investor Payments\n40% first round investors\n30% second round investors\n30% investors after second round' \
              '\n14%: Company Money Bank\n10%: Founding Team Payment\n* Max of $50 Million per individual per year' \
              '\n50% Andrei\n50% tbd\n6%: Service Cost\n-------------------------\n\nInvestment Money:' \
              '\n* This is default, each investor can choose their percentages *\n\n60%: Development Costs' \
              '\n100% development costs\n40%: Base Payment*\n* actually 0 for now" >> ' + str(text_doc.pk) + '.txt '

    command = "cd storage " \
              "\n cd organizations" \
              "\n cd " + organization_id + \
              "\n cd mains" \
              "\n cd git" \
              + text

    os.system(command)

    commitTextDocGit(text_doc.pk)
