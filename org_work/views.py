# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from org_home.models import Categories
from home.models import Organizations
from .models import Projects
from org_home.views import getCategoryAncestors

@login_required
def IndexView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request, 'org_work/index.html',{'organization': organization,'category':category,
                                                  'categories_list':Categories.objects.filter(organization=organization),
                                                  'ancestor_categories_list': ancestorCategories})

def ProjectView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_work/projects.html',{'organization': organization,'category':category,
                                                    'categories_list':Categories.objects.filter(organization=organization)})

def IndividualProjectView(request,organization_id,category_id,project_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    project = get_object_or_404(Projects,pk=project_id)
    ancestorCategories = getCategoryAncestors(category_id)
    return render(request,'org_work/individualProject.html',{'organization': organization,'category':category,
                                                    'categories_list':Categories.objects.filter(organization=organization),
                                                    'project':project, 'ancestor_categories_list': ancestorCategories
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

    commonProjects = []
    # initially populate list with the projects that belong to the first category
    category = get_object_or_404(Categories, pk=selectedIds[0])
    for proj in category.relatedCategory.all():
        commonProjects.append(proj)

    # remove all projects from commonProjects that isn't in all of the categories
    for catId in selectedIds:

        category = get_object_or_404(Categories, pk=catId)

        for proj in commonProjects:
            if proj not in category.relatedCategory.all():
                commonProjects.remove(proj)

    print(commonProjects)
    data = serializers.serialize('json', commonProjects)
    return HttpResponse(json.dumps(data), content_type='application/json')

# MUST REMOVE BELOW WHEN DONE

# # MUST REMOVE BELOW WHEN DONE (careful, parent is not longer charfield but foreignkey(self) )==
# @login_required
# def submitNewCategory(request,organization_id,category_id=None):
#     organization = get_object_or_404(Organizations,id=organization_id)
#     if request.method == "POST":
#         if 'new_category' in request.POST and request.POST['new_category'] != '':
#
#             # set access to category
#             closedCategory = False
#             gate_keeper = ''
#             if 'closed_category' in request.POST:
#                 closedCategory = True
#                 # gate_keeper is who can let people join the community. It can either be anyone in the community
#                 # or the moderator. access is the name of the radio field
#                 gate_keeper = request.POST['access']
#
#             # set category name
#             categoryName = request.POST['new_category']
#             formatedCategoryName = ' '.join(word[0].upper() + word[1:] for word in categoryName.split())
#             # returns error if the category name already exists
#             if Categories.objects.filter(organization=organization,category_name=formatedCategoryName).exists():
#                 return render(request, 'org_home/newCategory.html', {'organization':organization,'error_message': formatedCategoryName + " already exists.",})
#
#             # set parent
#             parent = None
#             if 'parent' in request.POST and request.POST['parent'] != "-1":
#                 parent = get_object_or_404(Categories,pk=int(request.POST['parent']))
#             else:
#                 # if has no parent make "executive" the parent of this category
#                 parent = Categories.objects.filter(organization=organization,category_name="Executive")[0]
#
#             # create the category
#             if parent.category_name == "Executive" or gate_keeper == '' or (gate_keeper == "all_members" and request.user in parent.members.all()) or (gate_keeper == "moderators" and request.user in parent.moderators.all()):
#                 category = Categories.objects.create(organization=organization,
#                                                      parent=parent,
#                                                      category_name=formatedCategoryName,
#                                                      closed_category = closedCategory,
#                                                      gateKeeper=gate_keeper)
#
#                 # add the creator to the members list
#                 category.members.add(request.user)
#
#                 # add creator as a moderator
#                 category.moderators.add(request.user)
#                 # add all parent mods to moderators list
#                 for p in parent.moderators.all():
#                     category.moderators.add(p)
#
#                 return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,category.id)))
#             else:
#                 return render(request, 'org_home/newCategory.html', {
#                 'organization':organization,
#                 'error_message': "You do not have permission to make new " + parent.category_name + " branch",
#             })
#         else:
#             return render(request, 'org_home/newCategory.html', {
#                 'organization':organization,
#                 'error_message': "Please enter at least one category.",
#             })
