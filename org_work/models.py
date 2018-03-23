# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from home import models as home_models
from org_home import models as org_home_models

class Projects(models.Model):
    organization = models.ForeignKey(home_models.Organizations, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(org_home_models.Categories, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    project_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name
