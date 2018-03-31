# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from home import models as home_models
# from org_home.models import Categories
# from django.contrib.auth.models import User
#
class Projects(models.Model):
#     organization = models.ForeignKey(home_models.Organizations, on_delete=models.CASCADE, blank=True, null=True)
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
#     parent = models.ForeignKey("self", blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    project_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name
