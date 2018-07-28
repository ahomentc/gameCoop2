# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Categories
from .models import Positions


class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('organization',               {'fields': ['organization']}),
        ('category_name', {'fields': ['category_name']}),
        ('parent',         {'fields': ['parent']}),
        ('moderators',         {'fields': ['moderators']}),
    ]

class PositionsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('category',               {'fields': ['category']}),
        ('position_name', {'fields': ['position_name']}),
    ]

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Positions, PositionsAdmin)
