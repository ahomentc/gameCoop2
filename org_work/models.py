# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from org_home.models import Categories
from home import models as home_models
from home.models import Organizations
from django.contrib.auth.models import User

# Should not have members because whoever is in the categories it belongs to is member.
class Projects(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ManyToManyField(Categories, blank=True, null=True, related_name='relatedCategory')
    parent = models.ForeignKey("self", blank=True, null=True, related_name='relatedParent')
    description = models.TextField(blank=True,null=True)
    project_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name


class WorkSubmissions(models.Model):
    class Meta:
        ordering = ['pub_date']

    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(default="", max_length=100)
    description = models.CharField(default="", max_length=1000)
    linkToSubmission = models.CharField(default="", max_length=1000)
    pub_date = models.DateTimeField('data published',blank=True,null=True)
    poster = models.ForeignKey(User, blank=True, null=True, related_name='posterName')
    user_up_votes = models.ManyToManyField(User, blank=True, null=True)
    accepted = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return self.title
