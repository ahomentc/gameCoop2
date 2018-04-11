# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Projects

from django.contrib import admin

class ProjectsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('organization',               {'fields': ['organization']}),
        ('category', {'fields': ['category']}),
        ('project_name', {'fields': ['project_name']}),
        ('parent',         {'fields': ['parent']}),
    ]

admin.site.register(Projects, ProjectsAdmin)
