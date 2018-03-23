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

from org_home.models import Categories
from home.models import Organizations
from .models import Projects
from .forms import NewProjectForm

@login_required
def IndexView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request, 'org_work/index.html',{'organization': organization,'category':category,
                                                  'categories_list':Categories.objects.filter(organization=organization)})

def ProjectView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_work/projects.html',{'organization': organization,'category':category,
                                                    'categories_list':Categories.objects.filter(organization=organization)})

# def newCategoryView(request,organization_id):
#     organization = get_object_or_404(Organizations,id=organization_id)
#     form = NewProjectForm()
#     parentsList = [("None","None")]
#     for proj in Projects.objects.filter(organization=organization):
#         parentsList.append((proj.project_name,proj.project_name))
#     form.fields['parent_branch'].choices = parentsList
#     return render(request, 'org_home/newCategory.html',{'organization':organization,'form':form})
