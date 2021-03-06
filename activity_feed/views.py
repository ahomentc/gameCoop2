from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.urls import reverse
from django.utils import timezone

from .models import ActivityPost
from home.models import Organizations
from org_home.models import Categories

import json
from django.http import JsonResponse

# called through url from javascript
def submitActivityClient(request):
    description = str(request.POST['description'])
    link_to_change = request.POST['link_to_change']

    activity = ActivityPost.objects.create(pub_date=timezone.now(),
                                           activity_description=description,
                                           link_to_change=link_to_change)

    activity.save()
    return HttpResponse("Success: submited activity")

# called from another view. I think this is the one we'll be using
def submitActivity(description, link_to_change, organization_id=None, category_id=None):
    organization = None
    category = None

    if(organization_id != None):
        organization = get_object_or_404(Organizations, id=organization_id)
    if(category_id != None):
        category = get_object_or_404(Categories, pk=category_id)

    activity = ActivityPost.objects.create(pub_date=timezone.now(),
                                           activity_description=description,
                                           link_to_change=link_to_change,
                                           category=category,
                                           organization=organization)
    activity.save()

def getActivities(request):
    organization_id = None
    category_id = None
    organization = None
    category = None

    if 'organization_id' in request.GET:
        organization_id = int(request.GET['organization_id'])
    if 'category_id' in request.GET:
        category_id = int(request.GET['category_id'])

    if organization_id != None:
        organization = get_object_or_404(Organizations, id=organization_id)
    if category_id != None:
        category = get_object_or_404(Categories, pk=category_id)

    recentActivityList = ActivityPost.objects.filter(
        organization=organization,
        category=category,
    ).order_by('-pub_date')[:10]

    recentActivityList = list(recentActivityList.values('activity_description', 'link_to_change', 'id', 'pub_date'))

    return JsonResponse(recentActivityList,safe=False)

