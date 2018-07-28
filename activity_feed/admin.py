from django.contrib import admin
from.models import ActivityPost

# Register your models here.
class ActivityPostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('activity_description',               {'fields': ['activity_description']}),
        ('link_to_change', {'fields': ['link_to_change']}),
        ('pub_date',         {'fields': ['pub_date']}),
    ]

admin.site.register(ActivityPost, ActivityPostAdmin)
