# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
from github import Github

import subprocess

from .models import Projects
from org_home.models import Categories
from home.models import Organizations

# https://www.fullstackpython.com/blog/first-steps-gitpython.html

def CreateGitRepo(request,organization_id,project_id):
    # project = get_object_or_404(Projects, pk=project_id)
    # organization = get_object_or_404(Organizations, pk=organization_id)
    # name = project.project_name.replace(' ','_')

    command = "cd storage " \
              "\n cd organizations" \
              "\n mkdir " + organization_id + \
              "\n cd " + organization_id + \
              "\n mkdir categories" \
              "\n mkdir projects" \
              "\n cd projects" \
              "\n mkdir " + project_id + \
              "\n cd " + project_id + \
              "\n mkdir git" \
              "\n cd git" \
              "\n git init"
    os.system(command)

    return HttpResponse(status=204)

# https://stackoverflow.com/questions/20291731/how-to-connect-to-a-remote-git-repository

def ConnectGitHub(request,organization_id,project_id):
    project = get_object_or_404(Projects, pk=project_id)
    organization = get_object_or_404(Organizations, pk=organization_id)
    org_name = organization.organization_name.replace(' ','_')
    proj_name = project.project_name.replace(' ','_')

    # # using username and password
    # g = Github("user", "password")

    # or using an access token
    g = Github("b48339464380cfb1f9cd4d0233e57de1834cdbf5")
    org = g.get_organization('GroupRoots')
    repoName = organization_id + "_" + project_id + "-" + org_name + "_" + proj_name
    try:
        repo = org.create_repo(repoName)
    except:
        pass
    # maybe next step is to create github organizations for each
    return HttpResponse(status=204)

def getGitURL(request, organization_id, organization_name, project_id, project_name):
    org_name = organization_name.replace(' ', '_')
    proj_name = project_name.replace(' ', '_')
    repoName = organization_id + "_" + project_id + "-" + org_name + "_" + proj_name
    URL = "https://github.com/GroupRoots/" + repoName

    return HttpResponse(URL)

# https://stackoverflow.com/questions/49458329/create-clone-and-push-to-github-repo-using-pygithub-and-pygit2

# how to keep track of activity if using github? Also, how can only push if community/mod votes yes?
# https://github.com/features/code-review/
# Maybe make me the superuser for all the repositories and then I can control what happens and the community through me.
