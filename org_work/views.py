# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from org_home.models import Categories
from home.models import Organizations
from .models import Projects
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

# submit a new category
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


def SubmitWorkView(request,organization_id, project_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    project = get_object_or_404(Projects, pk=project_id)

    projects_list = Projects.objects.filter(organization=organization)
    return render(request, 'org_work/submitWork.html', {'organization': organization,
                                                               'categories_list': Categories.objects.filter(organization=organization),
                                                               'project': project,
                                                               'projects_list': projects_list
                                                               })
