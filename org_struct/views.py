# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
import os

from django.shortcuts import render
from home.models import Organizations
from consensusEditing.models import TextDoc

@login_required
def IndexView(request, organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    monetaryDistributionDoc = get_object_or_404(TextDoc, title="Monetary Distribution", organization=organization, isMain = True)
    return render(request, 'org_struct/index.html',{'organization':organization,
                                                    'monetaryDistributionDoc':monetaryDistributionDoc,
                                                    })

# @login_required
# def MoneyDistributionView(request, organization_id):
#     organization = get_object_or_404(Organizations,id=organization_id)
#
#     # get the text file
#     path = "/Users/andrei/gameCoop2/storage/organizations/" + organization_id + "/git/monetaryDistribution.txt"
#     with open(path, 'r') as f:
#         text = f.read()
#
#     return render(request, 'org_struct/monetary_distribution.html',{'organization':organization,'text':text})
#
# def community_editing(request, organization_id):
#     organization = get_object_or_404(Organizations, id=organization_id)
#
#     text = request.POST['content']
#
#     path = "/Users/andrei/gameCoop2/storage/organizations/" + organization_id + "/git/monetaryDistribution" + str(request.user.id) + ".txt"
#     with open(path, 'w') as f:
#         f.write(text)
#
#     return render(request, 'org_struct/monetary_distribution.html', {'organization': organization,'text':text})
