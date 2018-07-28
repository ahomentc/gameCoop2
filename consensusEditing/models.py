from django.db import models
from org_home.models import Categories
from home.models import Organizations
from org_work.models import Projects
from django.contrib.auth.models import User

class TextDoc(models.Model):
    # Title and description of the document
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    # Who created the document. Empty if automatically created
    poster = models.OneToOneField(User,blank=True, null=True)

    # Organization, Category, or Project
    location_type = models.CharField(max_length=100)
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Projects, blank=True, null=True)

    # If the document is the main document or a proposal (proposal is like a branch)
    isMain = models.BooleanField()
    # relation between this document and its main document
    mainDoc = models.ForeignKey("self", blank=True, null=True)

    # path to the document in the filesystem
    pathToFile = models.CharField(max_length=500)
    # pathToFile = models.URLField()

class vote(models.Model):
    textDoc = models.ForeignKey(TextDoc, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User)
