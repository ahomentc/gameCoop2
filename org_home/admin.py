# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Categories


class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('organization',               {'fields': ['organization']}),
        ('category_name', {'fields': ['category_name']}),
        ('parent',         {'fields': ['parent']}),
        ('moderators',         {'fields': ['moderators']}),
    ]

admin.site.register(Categories, CategoriesAdmin)
