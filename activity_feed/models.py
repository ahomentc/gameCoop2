from django.db import models
from home import models as home_models
from org_home import models as org_home_models

# activity vs issues? Answer: Activity. Issues will be in the "Decisions" page which will replace "Vote"

# Create your models here.
class ActivityPost(models.Model):
    class Meta:
        ordering = ['pub_date']

    organization = models.ForeignKey(home_models.Organizations, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(org_home_models.Categories, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    activity_description = models.CharField(max_length=100)
    link_to_change = models.CharField(max_length=500)

    # type = models.CharField(max_length=100)  #tentative
