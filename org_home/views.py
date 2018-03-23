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

from .models import Categories
from home.models import Organizations
from .forms import ParentCategories

# org_home page of a coop
@login_required
def IndexView(request,organization_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    return render(request, 'org_home/index.html',{'organization': organization,'member_categories_list': Categories.objects.filter(
        members__id=request.user.id,organization=organization),
        'categories_list':Categories.objects.filter(organization=organization)
    })

# list of all the categories/root/branch in a coop
@login_required
def CategoryView(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/categories.html',{'organization':organization,'categories_list':Categories.objects.filter(organization=organization)})

# org_home page of specific category/root/branch in a coop
@login_required
def IndividualCategoryView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    subCategories = Categories.objects.filter(parent=category)
    return render(request,'org_home/individualCategory.html',{'organization':organization,'category': category,'subCategories':subCategories,
        'categories_list':Categories.objects.filter(organization=organization)})

# page to create a new category/root/branch
@login_required
def newCategoryView(request,organization_id,category_id=None):
    organization = get_object_or_404(Organizations,id=organization_id)
    if category_id != None:
        category = get_object_or_404(Categories,pk=category_id)
    else:
        category = None
    form = ParentCategories()
    parentsList = [("None","None")]
    for cat in Categories.objects.filter(organization=organization,parent=category):
        parentsList.append((cat.category_name,cat.category_name))
    return render(request, 'org_home/newCategory.html',{'organization':organization,'category':category,
                                                        'categories_list':Categories.objects.filter(organization=organization)})

# submit a new category
@login_required
def submitNewCategory(request,organization_id,category_id=None):
    organization = get_object_or_404(Organizations,id=organization_id)
    if request.method == "POST":
        if 'new_category' in request.POST and request.POST['new_category'] != '':

            # set access to category
            closedCategory = False
            gate_keeper = ''
            if 'closed_category' in request.POST:
                closedCategory = True
                # gate_keeper is who can let people join the community. It can either be anyone in the community
                # or the moderator. access is the name of the radio field
                gate_keeper = request.POST['access']

            # set category name
            categoryName = request.POST['new_category']
            formatedCategoryName = ' '.join(word[0].upper() + word[1:] for word in categoryName.split())
            # returns error if the category name already exists
            if Categories.objects.filter(organization=organization,category_name=formatedCategoryName).exists():
                return render(request, 'org_home/newCategory.html', {'organization':organization,'error_message': formatedCategoryName + " already exists.",})

            # set parent
            parent = None
            if 'parent' in request.POST and request.POST['parent'] != "-1":
                parent = get_object_or_404(Categories,pk=int(request.POST['parent']))
            else:
                # if has no parent make "executive" the parent of this category
                parent = Categories.objects.filter(organization=organization,category_name="Executive")[0]

            # create the category
            if parent.category_name == "Executive" or gate_keeper == '' or (gate_keeper == "all_members" and request.user in parent.members.all()) or (gate_keeper == "moderators" and request.user in parent.moderators.all()):
                category = Categories.objects.create(organization=organization,
                                                     parent=parent,
                                                     category_name=formatedCategoryName,
                                                     closed_category = closedCategory,
                                                     gateKeeper=gate_keeper)

                # add the creator to the members list
                category.members.add(request.user)

                # add creator as a moderator
                category.moderators.add(request.user)
                # add all parent mods to moderators list
                for p in parent.moderators.all():
                    category.moderators.add(p)

                return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,category.id)))
            else:
                return render(request, 'org_home/newCategory.html', {
                'organization':organization,
                'error_message': "You do not have permission to make new " + parent.category_name + " branch",
            })
        else:
            return render(request, 'org_home/newCategory.html', {
                'organization':organization,
                'error_message': "Please enter at least one category.",
            })

# category access #

# list of all members in a category
@login_required
def membersView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_home/members.html',{'organization':organization,'category': category,
                                                   'categories_list':Categories.objects.filter(organization=organization)})

# list of pending members in a category
@login_required
def pendingMembersView(request,organization_id,category_id):
    # this html is also called in GrantAccess
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_home/pendingMembers.html',{'organization':organization,'category': category,
                                                          'categories_list':Categories.objects.filter(organization=organization)})

# list of all moderators in a category
@login_required
def modsView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_home/members.html',{'organization':organization,'category': category,
                                                   'categories_list':Categories.objects.filter(organization=organization)})

# join a category
@login_required
def JoinCategory(request,organization_id,category_id):
    '''
    if open category, add user to members list of category
    if closed category, add user to pending_members list of category
    '''
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    parent = Categories.objects.filter(organization=organization,category_name=category.parent)[0]

    if request.user in parent.members.all():
        category.members.add(request.user)
    else:
        if category.closed_category == False:
            category.members.add(request.user)
        else:
            category.pending_members.add(request.user)
    return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,category.id,)))

# grant access to someone to become a member of a category
@login_required
def GrantAccess(request,organization_id,category_id,pending_member_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    pending_member = User.objects.get(pk=pending_member_id)

    # if any member can add pending members to category
    if category.gateKeeper == 'all_members':
        if request.user in category.members.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
    # if only moderator can add pending members to category
    elif category.gateKeeper == 'moderators':
        if request.user in category.moderators.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
        else:
            return render(request,'org_home/pendingMembers.html',{'organization':organization,'category': category,'error_message':'Must be a moderator to add user to ' +  category.category_name })
    return HttpResponseRedirect(reverse('org_home:pendingMembersView', args=(organization.id,category.id,)))



# organization access #

# list of all members in an organization
@login_required
def orgMembersView(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/org_members.html',{'organization':organization,})

# list of pending members in an organization
@login_required
def orgPendingMembersView(request,organization_id):
    # this html is also called in GrantAccess
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/org_pending_members.html',{'organization':organization,})

# join the organization
@login_required
def JoinOrganization(request,organization_id):
    '''
    if open organization, add user to members list of org
    if closed org, add user to pending_members list of org
    '''
    organization = get_object_or_404(Organizations,id=organization_id)
    # if org is open
    if organization.closed_organization == False:
        organization.members.add(request.user)
    else:
        organization.pending_members.add(request.user)
    return HttpResponseRedirect(reverse('org_home:index', args=(organization.id,)))

# grant access to someone to become a member of an organization
@login_required
def GrantAccessToOrg(request,organization_id,pending_member_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    pending_member = User.objects.get(pk=pending_member_id)

    # if any member can add pending members to category
    if organization.gateKeeper == 'all_members':
        if request.user in organization.members.all():
            organization.members.add(pending_member)
            organization.pending_members.remove(pending_member)
    # if only moderator can add pending members to category
    elif organization.gateKeeper == 'moderators':
        if request.user in organization.moderators.all():
            organization.members.add(pending_member)
            organization.pending_members.remove(pending_member)
        else:
            return render(request,'org_home/org_pending_members.html',{'organization':organization,'error_message':'Must be a moderator to add user to ' +  organization })
    return HttpResponseRedirect(reverse('org_home:orgPendingMembersView', args=(organization.id,)))
