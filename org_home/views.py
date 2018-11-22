# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Categories
from .models import Positions
from org_work.models import Projects
from org_work.models import WorkSubmissions
from home.models import Organizations
from .forms import ParentCategories


# ------------------------------------------------------------------------------------------------ #
# organization
#

# org_home page of a coop
@login_required
def IndexView(request,organization_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    userPercentageInOrg = round(getUserPercentageInOrg(organization, request.user) * 100,3)
    return render(request, 'org_home/index.html',
                  { 'organization': organization,
                    'member_categories_list': Categories.objects.filter(members__id=request.user.id,organization=organization),
                    'categories_list':Categories.objects.filter(organization=organization),
                    'projects_list': Projects.objects.filter(organization=organization),
                    'userPercentageInOrg': userPercentageInOrg,
                  })

# list of all members in an organization
@login_required
def orgMembersView(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/org_members.html',{'organization':organization,'categories_list':Categories.objects.filter(organization=organization)})

# list of pending members in an organization
@login_required
def orgPendingMembersView(request,organization_id):
    # this html is also called in GrantAccess
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/org_pending_members.html',{'organization':organization,'categories_list':Categories.objects.filter(organization=organization)})

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


# ------------------------------------------------------------------------------------------------ #
# category... aka Department or Branch (within Organization)
#


# list of all the categories/root/branch in a coop DELETE THIS I THINK
@login_required
def CategoryView(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/categories.html',{'organization':organization,'categories_list':Categories.objects.filter(organization=organization)})

# org_home page of specific category/root/branch in a coop
@login_required
def IndividualCategoryView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    real_cat = category
    subCategories = Categories.objects.filter(parent=category)
    ancestorCategories = getCategoryAncestors(category_id)
    projects_list = Projects.objects.filter(organization=organization,category=category)

    if category.needAcceptedContribs:
        submissionsList = WorkSubmissions.objects.filter(
                organization=organization,
                category=category,
                accepted=True,
            ).order_by('-pub_date')[:10]
    else:
        submissionsList = WorkSubmissions.objects.filter(
                organization=organization,
                category=category,
            ).order_by('-pub_date')[:10]
    
    no_subs_message=""
    if len(submissionsList) == 0:
        no_subs_message = "No submissions here yet"

    contribsUserLiked = getContribsUserLiked(request.user, organization, category)

    num_pending = WorkSubmissions.objects.filter(
                organization=organization,
                category=category,
                accepted=False,
                ).count()

    return render(request,'org_home/individualCategory.html',{'organization':organization,
                                                            'category': category,
                                                            'real_cat' : real_cat,
                                                            'subCategories':subCategories,
                                                            'categories_list':Categories.objects.filter(organization=organization,),
                                                            'ancestor_categories_list':ancestorCategories,
                                                            'projects_list':projects_list,
                                                            'submissionsList': submissionsList,
                                                            'no_subs_message': no_subs_message,
                                                            'contribsUserLiked': contribsUserLiked,
                                                            'num_pending': num_pending,
                                                            })

# --- helper functions -----

def getCategoryAncestors(category_id):
    currentCategory = get_object_or_404(Categories,pk=category_id)
    ancestors = []
    while currentCategory.parent != None:
        ancestors.insert(0,currentCategory.parent)
        currentCategory = currentCategory.parent
    return ancestors

@csrf_exempt
def userInCategory(request):
    category_id = int(request.POST.get('category_id'))
    category = get_object_or_404(Categories, pk=category_id)
    if request.user in category.members.all():
        return HttpResponse(1)
    return HttpResponse(0)

def getContribsUserLiked(user, organization, category):
    allContribs = WorkSubmissions.objects.filter(organization=organization,category=category)
    contribs = []
    for contrib in allContribs:
        if user in contrib.user_up_votes.all():
            contribs.append(contrib)
    return contribs

# def getUserPercentageInCategory(organization, category, user):
#     # total number of points in category (post * likes per post)
#     numCategoryPoints = 0

#     # total number of points user has in category
#     numUserPointsInCat = 0

#     # get all the submissions in the category
#     categorySubmissions = WorkSubmissions.objects.filter(organization=organization, category=category)
#     for submission in categorySubmissions:
#         numCategoryPoints += (1 + submission.user_up_votes.count())



#     userSubmissions = WorkSubmissions.objects.filter(organization=organization, category=category, poster=user)
#     for submission in userSubmissions:
#         numUserPointsInCat += (1 + submission.user_up_votes.count())

#     if(numCategoryPoints > 0):
#         percentUsersSubsInCat = numUserPointsInCat / numCategoryPoints
#         return percentUsersSubsInCat

#     return 0

def getUserPercentageInOrg(organization, user):
    # total number of points in org (post * likes per post)
    numOrgPoints = 0

    # total number of points user has in category
    numUserPointsInOrg = 0

    # get all the submissions in the category
    orgSubmissions = WorkSubmissions.objects.filter(organization=organization, accepted=True)
    for submission in orgSubmissions:
        numOrgPoints += (1 + submission.user_up_votes.count())

    userSubmissions = WorkSubmissions.objects.filter(organization=organization, poster=user, accepted=True)

    for submission in userSubmissions:
        numUserPointsInOrg += (1 + submission.user_up_votes.count())

    if(numOrgPoints > 0):
        percentUsersSubsInOrg = numUserPointsInOrg / numOrgPoints
        return percentUsersSubsInOrg

    return 0

# ---- creating a new category -----

# page to create a new category/root/branch
@login_required
def newCategoryView(request,organization_id,category_id=None):
    organization = get_object_or_404(Organizations,id=organization_id)
    ancestorCategories = None
    category = None
    if category_id != None:
        category = get_object_or_404(Categories,pk=category_id)
        ancestorCategories = getCategoryAncestors(category_id)

    return render(request, 'org_home/newCategory.html',{'organization':organization,'category':category,
                                                        'categories_list':Categories.objects.filter(organization=organization),
                                                            'ancestor_categories_list':ancestorCategories})

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

            moderator_work_approval = False
            if 'moderator_work_approval' in request.POST and request.POST['moderator_work_approval'] == "on":
                moderator_work_approval = True

            # create the category
            if parent.category_name == "Executive" or gate_keeper == '' or (gate_keeper == "all_members" and request.user in parent.members.all()) or (gate_keeper == "moderators" and request.user in parent.moderators.all()):
                category = Categories.objects.create(organization=organization,
                                                     parent=parent,
                                                     category_name=formatedCategoryName,
                                                     closed_category = closedCategory,
                                                     gateKeeper=gate_keeper,
                                                     needAcceptedContribs=moderator_work_approval,)

                # add the creator to the members list
                category.members.add(request.user)

                # add creator as a moderator
                category.moderators.add(request.user)
                # add all parent mods to moderators list
                for p in parent.moderators.all():
                    category.moderators.add(p)

                category.save()

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

# --- information within category -----

# list of all members in a category
@login_required
def membersView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_home/members.html',{'organization':organization,'category': category,
                                                   'categories_list':Categories.objects.filter(organization=organization)})

# list of pending members in a category
@login_required
def pendingMembersView(request,organization_id,category_id):
    # this html is also called in GrantAccess
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_home/pendingMembers.html',{'organization':organization,'category': category,
                                                          'categories_list':Categories.objects.filter(organization=organization)})

# list of all moderators in a category
@login_required
def modsView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_home/moderators.html',{'organization':organization,'category': category,
                                                   'categories_list':Categories.objects.filter(organization=organization)})


# ---- Joining and Granting access to category ----
# join a category
@login_required
def JoinCategory(request,organization_id,category_id):
    '''
    if open category, add user to members list of category
    if closed category, add user to pending_members list of category
    '''
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    if category.category_name != "Executive":
        parent = Categories.objects.filter(organization=organization,category_name=category.parent)[0]
        if request.user in parent.members.all():
            category.members.add(request.user)
        else:
            if category.closed_category == False:
                category.members.add(request.user)
            else:
                category.pending_members.add(request.user)
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
            category.save()
    # if only moderator can add pending members to category
    elif category.gateKeeper == 'moderators':
        if request.user in category.moderators.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
            category.save()
        else:
            return render(request,'org_home/pendingMembers.html',{'organization':organization,'category': category,
                                                                  'error_message':'Must be a moderator to add user to ' +  category.category_name })
    return HttpResponseRedirect(reverse('org_home:pendingMembersView', args=(organization.id,category.id,)))

# make someone a moderator (ajax)
@login_required
def makeMod(request):
    category_id = int(request.POST.get('category_id'))
    new_mod_id = int(request.POST.get('new_mod_id'))

    category = get_object_or_404(Categories,pk=category_id)
    new_mod = User.objects.get(pk=new_mod_id)

    if request.user in category.moderators.all():
        category.moderators.add(new_mod)
        return HttpResponse("Success: Moderator Added")

    else:
        return HttpResponse("error: must be moderator")



# ------------------------------------------------------------------------------------------------ #
# Positions (in category)
#

@login_required
def positionsView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    positions = Positions.objects.filter(category=category)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_home/positions.html',{'organization':organization,'category': category,'positions': positions,
                                                   'categories_list':Categories.objects.filter(organization=organization)})

@login_required
def individualPosition(request,organization_id,category_id,position_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    position = get_object_or_404(Positions, pk=position_id)
    users = position.position_holders
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_home/individualPosition.html',{'organization':organization,'category': category,'position': position,'users':users,
                                                   'categories_list':Categories.objects.filter(organization=organization)})

@login_required
def newPositionView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    positions = Positions.objects.filter(category=category)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_home/newPosition.html',{'organization':organization,'category': category,'positions': positions,
                                                   'categories_list':Categories.objects.filter(organization=organization)})

def submitNewPosition(request,organization_id,category_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    category = get_object_or_404(Categories, pk=category_id)
    positions = Positions.objects.filter(category=category)

    description = request.POST['positionDescription']
    positionName = request.POST['positionName']
    membersInPos = request.POST.getlist('membersInPos')

    position = Positions.objects.create(category=category,
                                        position_name=positionName,
                                        description=description)

    position.save()

    for userId in membersInPos:
        posUser = User.objects.filter(pk=userId)[0]
        position.position_holders.add(posUser)
        position.save()

    position.save()

    return render(request, 'org_home/positions.html',
                  {'organization': organization, 'category': category, 'positions': positions,
                   'categories_list': Categories.objects.filter(organization=organization)})

@csrf_exempt
def requestToJoinPos(request):
    position_id = int(request.POST['position_id'])
    position = get_object_or_404(Positions, pk=position_id)
    try:
        position.position_requesters.add(request.user)
        position.save()
        return HttpResponse("Success: Added user")
    except Exception as e:
        return "Error: " + str(e)

@csrf_exempt
def grantAccessToPosition(request):

    # !! in the future make it so that either the position holders or community vote
    # !! or anybody who has the position or is an admin can grant access

    position_id = int(request.POST['position_id'])
    user_id = int(request.POST['user_id'])
    position = get_object_or_404(Positions, pk=position_id)
    requested_user = get_object_or_404(User, pk=user_id)

    position.position_holders.add(requested_user)
    position.position_requesters.remove(requested_user)
    position.save()

    return HttpResponse("Success: User Added")

