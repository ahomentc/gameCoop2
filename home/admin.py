# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Organizations

class OrganizationsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('organization_name',               {'fields': ['organization_name']}),
        ('closed_organization',               {'fields': ['closed_organization']}),
    ]
admin.site.register(Organizations, OrganizationsAdmin)
