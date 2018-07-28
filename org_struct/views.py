# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from home.models import Organizations
from org_home.models import Categories
from consensusEditing.models import TextDoc

@login_required
def IndexView(request, organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    monetaryDistributionDoc = get_object_or_404(TextDoc, title="Monetary Distribution", organization=organization, isMain = True)
    return render(request, 'org_struct/index.html',{'organization':organization,
                                                    'categories_list': Categories.objects.filter(organization=organization, ),
                                                    'monetaryDistributionDoc':monetaryDistributionDoc,
                                                    })

