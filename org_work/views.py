# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone
import json

from org_home.models import Categories
from home.models import Organizations
from .models import Projects
from .models import WorkSubmissions
from org_home.views import getCategoryAncestors

def getProjectAncestors(project_id):
    currentProject = get_object_or_404(Projects,pk=project_id)
    ancestors = []
    while currentProject.parent != None:
        ancestors.insert(0,currentProject.parent)
        currentProject = currentProject.parent
    return ancestors

@login_required
def IndexView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    ancestorCategories = getCategoryAncestors(category_id)
    projects_list = Projects.objects.filter(organization=organization)


    # ancestorProjects = getProjectAncestors()
    return render(request, 'org_work/index.html',{'organization': organization,'category':category,
                                                  'categories_list':Categories.objects.filter(organization=organization),
                                                  'ancestor_categories_list': ancestorCategories,
                                                  'projects_list':projects_list
                                                  })

def ProjectView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_work/projects.html',{'organization': organization,'category':category,
                                                    'categories_list':Categories.objects.filter(organization=organization)})

def IndividualProjectView(request,organization_id, project_id, category_id=None):
    organization = get_object_or_404(Organizations,pk=organization_id)
    project = get_object_or_404(Projects, pk=project_id)
    if category_id != None:
        category = get_object_or_404(Categories,pk=category_id)
        ancestorCategories = getCategoryAncestors(category_id)
        projects_list = Projects.objects.filter(organization=organization, category=category)
        return render(request,'org_work/individualProject.html',{'organization': organization,'category':category,
                                                        'categories_list':Categories.objects.filter(organization=organization),
                                                        'project':project,
                                                        'ancestor_categories_list': ancestorCategories,
                                                        'projects_list': projects_list
                                                        })
    projects_list = Projects.objects.filter(organization=organization)
    return render(request, 'org_work/individualProject.html', {'organization': organization,
                                                               'categories_list': Categories.objects.filter(organization=organization),
                                                               'project': project,
                                                               'projects_list': projects_list
                                                               })

def newProjectView(request,organization_id,category_id=None,parent_id=None):
    # one of the organizations the project belongs to (just need one bc of naviagtion and already on the org page)
    organization = get_object_or_404(Organizations,id=organization_id)
    ancestorCategories = getCategoryAncestors(category_id)

    # one of the categories the project belongs to.
    category = None
    if category_id != None:
        category = get_object_or_404(Categories,pk=category_id)

    parent = None
    if parent_id != None:
        parent = get_object_or_404(Projects,pk=parent_id)

    return render(request, 'org_work/newProject.html',{'organization':organization,'category':category,
                                                       'categories_list': Categories.objects.filter(organization=organization),
                                                        'ancestor_categories_list':ancestorCategories})

@csrf_exempt
def ProjectsInCommon(request):
    selectedIds = json.loads(request.POST['selectedIds'])
    selectedTreePositions = json.loads(request.POST['selectedTreePositions'])
    maxPosition = int(request.POST.get('maxTreePositions'))
    currentPosition = maxPosition

    commonProjects = set()
    # set of categories that have projects in common
    commonProjectCategories = set()

    # iterate twice so that updates
    k=2
    while k > 0:
        for i,(id,pos) in enumerate(zip(selectedIds,selectedTreePositions)):
            category = get_object_or_404(Categories, pk=selectedIds[i])
            # populate the commonProjects with all projects of category
            if len(commonProjects) == 0 or childInSet(category,commonProjectCategories) or parentInSet(category,commonProjectCategories):
                for proj in category.relatedCategory.all():
                    commonProjects.add(proj)
                    commonProjectCategories.add(category)
            else:
                for proj in commonProjects:
                    if proj not in category.relatedCategory.all():
                        commonProjects.discard(proj)
                        commonProjectCategories.discard(category)
        k-=1

        currentPosition -= 1
    data = serializers.serialize('json', commonProjects)
    return HttpResponse(json.dumps(data), content_type='application/json')

def childInSet(category,set):
    if len(category.category_parent.all()) == 0:
        return category in set
    elif category in set:
        return True
    else:
        for child in category.category_parent.all():
            if childInSet(child,set):
                return True
    return False

def parentInSet(category,set):
    if category.parent == None:
        return category in set
    elif category.parent in set:
        return True
    else:
        return parentInSet(category.parent,set)

# submit a new project
@login_required
def submitNewProject(request, organization_id, original_cat=None):
    organization = get_object_or_404(Organizations,id=organization_id)
    if request.method == "POST":
        if 'new_project' in request.POST and request.POST['new_project'] != '':

            # set project name
            projectName = request.POST['new_project']
            formatedProjectName = ' '.join(word[0].upper() + word[1:] for word in projectName.split())
            # returns error if the category name already exists
            if Projects.objects.filter(organization=organization,project_name=formatedProjectName).exists():
                return render(request, 'org_work/newProject.html', {'organization':organization,'error_message': formatedProjectName + " already exists.",})

            # set categories
            categoriesIds = None
            if 'categoryCheckbox' in request.POST and len(request.POST.getlist('categoryCheckbox'))>0:
                categoriesIds = request.POST.getlist('categoryCheckbox')


            # set parent project
            parent = None
            if 'parent' in request.POST and request.POST['parent'] != "-1":
                parent = get_object_or_404(Projects,pk=int(request.POST['parent']))
                print(parent)

            # create the category
            if True: #add some conditions here based on the conditions of the category they're in
                project = Projects.objects.create(organization=organization,
                                                     parent=parent,
                                                     project_name=formatedProjectName,
                                                    )
                # maybe add a members list

                # add the categories
                for cat_id in categoriesIds:
                    cat = get_object_or_404(Categories,id=cat_id)
                    project.category.add(cat)

                if original_cat == None:
                    original_cat = categoriesIds[0]

                return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,original_cat)))
            else:
                return render(request, 'org_work/newProject.html', {
                'organization':organization,
                'category': original_cat,
                'error_message': "You do not have permission to make new " + parent.category_name + " branch",
            })
        else:
            return render(request, 'org_work/newProject.html', {
                'organization':organization,
                'category': original_cat,
                'error_message': "Please enter at least one category.",
            })


# submit new work 

def SubmitWorkView(request,organization_id, category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories, pk=category_id)

    return render(request, 'org_work/submitWork.html', {'organization': organization,
                                                               'categories_list': Categories.objects.filter(organization=organization),
                                                               'category': category,
                                                               })


def submitWork(request, organization_id, category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories, pk=category_id)

    if request.method == "POST":
        if 'title' in request.POST and request.POST['title'] != '' and 'urlToSubmission' in request.POST and request.POST['urlToSubmission'] != '':
            title = request.POST['title']
            description = ''
            if 'description' in request.POST:
                description = request.POST['description']
            urlToSubmission = request.POST['urlToSubmission']
            if "http" not in urlToSubmission:
                urlToSubmission = "http://" + urlToSubmission

            work = WorkSubmissions.objects.create(
                organization=organization, 
                category=category, 
                title=title, 
                description=description, 
                linkToSubmission=urlToSubmission, 
                pub_date=timezone.now(),
                poster=request.user,
                accepted=False)

            if request.user in category.moderators.all() or category.needAcceptedContribs == False:
                work.accepted=True
                work.save()

            return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization_id,category_id)))

        else:
            return render(request, 'org_work/submitWork.html', {'organization': organization,
                                                               'categories_list': Categories.objects.filter(organization=organization),
                                                               'category': category,
                                                               'error_message': "You must have a title and a link to your work",
                                                               })


#vote for a submission
def voteForContrib(request):
    contrib_id = int(request.POST.get('id'))
    vote_action = request.POST.get('action')

    submission = get_object_or_404(WorkSubmissions, pk=contrib_id)

    thisUserUpVote = submission.user_up_votes.filter(id = request.user.id).count()

    if (vote_action == 'vote'):
        if(thisUserUpVote == 0):
            submission.user_up_votes.add(request.user)
        else:
            return HttpResponse('error - already voted')
    elif (vote_action == 'recall-vote'):
        if (thisUserUpVote == 1):
            submission.user_up_votes.remove(request.user)
        else:
            return HttpResponse('error - unknown vote type or no vote to recall')
    else:
        return HttpResponse('error - bad action')
    num_votes = submission.user_up_votes.count()
    return HttpResponse(num_votes)


def pendingWork(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    real_cat = category
    subCategories = Categories.objects.filter(parent=category)
    ancestorCategories = getCategoryAncestors(category_id)

    submissionsList = WorkSubmissions.objects.filter(
                organization=organization,
                category=category,
                accepted=False,
            ).order_by('-pub_date')[:10]
    
    no_subs_message=""
    if len(submissionsList) == 0:
        no_subs_message = "All submissions accepted"

    return render(request,'org_work/pendingWork.html',{'organization':organization,
                                                            'category': category,
                                                            'real_cat' : real_cat,
                                                            'subCategories':subCategories,
                                                            'categories_list':Categories.objects.filter(organization=organization,),
                                                            'ancestor_categories_list':ancestorCategories,
                                                            'submissionsList': submissionsList,
                                                            'no_subs_message': no_subs_message,
                                                            })


# accept for a submission
def acceptRejectWork(request):
    contrib_id = int(request.POST.get('id'))
    action = request.POST.get('action')

    if action == "reject":
        submission = get_object_or_404(WorkSubmissions, pk=contrib_id)
        # delete the submission
        submission.delete()
        return HttpResponse('success')
    if action == "accept":
        submission = get_object_or_404(WorkSubmissions, pk=contrib_id)
        submission.accepted = True
        submission.save()
        return HttpResponse('success')
    return HttpResponse('error')




