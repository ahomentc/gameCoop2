# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Organizations(models.Model):
    organization_name = models.CharField(max_length=100)
    pending_members = models.ManyToManyField(User,related_name='organization_pending_member')
    members = models.ManyToManyField(User,related_name='organization_member')
    moderators = models.ManyToManyField(User,related_name='organization_super_member')
    closed_organization = models.BooleanField()
    gateKeeper = models.CharField(max_length=30) # either all_members or moderators

    def __str__(self):
        return self.organization_name
