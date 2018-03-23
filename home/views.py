# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Organizations
from org_home.models import Categories

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

        return HttpResponseRedirect(reverse('home:organizations'))
    else:
        return render(request, 'home/newOrganization.html', {
            'error_message': "Please enter a organization.",
        })
