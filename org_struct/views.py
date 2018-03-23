# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from home.models import Organizations

@login_required
def IndexView(request, organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request, 'org_struct/index.html',{'organization':organization})

@login_required
def MoneyDistributionView(request, organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request, 'org_struct/monetary_distribution.html',{'organization':organization})
