# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from org_home.models import Categories
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def ProfileView(request,user):
    selected_user = get_object_or_404(User, username=user)
    return render(request,'user_profiles/profile.html',{'member_categories_list': Categories.objects.filter(
        members__id=selected_user.id)
    })
