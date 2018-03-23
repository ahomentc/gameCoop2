# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from org_home import models as org_home_models
from django.contrib.auth.models import User

class Post(models.Model):
    class Meta:
        ordering = ['pub_date']

    discussionType = models.CharField(max_length=100)
    category = models.ForeignKey(org_home_models.Categories,on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    original_poster = models.ForeignKey(User,blank=True,null=True)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    userUpVotes = models.ManyToManyField(User, blank=True, related_name='PostUpVotes')
    userDownVotes = models.ManyToManyField(User, blank=True, related_name='PostDownVotes')

class Reply(models.Model):
    class Meta:
        ordering = ['pub_date']

    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True)
    content = models.TextField()
    user = models.ForeignKey(User,blank=True,null=True)
    pub_date = models.DateTimeField('data published',blank=True,null=True)
    userUpVotes = models.ManyToManyField(User, blank=True, related_name='RepliesUpVotes')
    userDownVotes = models.ManyToManyField(User, blank=True, related_name='RepliesDownVotes')
