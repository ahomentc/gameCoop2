# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from home import models as home_models
from org_work.models import Projects

class Categories(models.Model):
    organization = models.ForeignKey(home_models.Organizations, on_delete=models.CASCADE, blank=True, null=True)
    # parent = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True)
    category_name = models.CharField(max_length=100)
    pending_members = models.ManyToManyField(User,related_name='category_pending_member')
    members = models.ManyToManyField(User,related_name='category_member')
    moderators = models.ManyToManyField(User,related_name='category_super_member')

    # when a parental moderator clicks join to the community, he becomes a regular moderator
    parentalModerators = models.ManyToManyField(User,related_name='category_parental_mod')

    closed_category = models.BooleanField()
    gateKeeper = models.CharField(max_length=30) # either all_members or moderators

    projects = models.ManyToManyField(Projects, blank=True, null=True)

    def __str__(self):
        return self.category_name
