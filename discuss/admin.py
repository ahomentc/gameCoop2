# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post,Reply

class RepliesInline(admin.StackedInline):
    model = Reply
    extra = 3

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('discussionType',               {'fields': ['discussionType'],}),
        ('title',               {'fields': ['title'],}),
        ('content',               {'fields': ['content'],}),
    ]
    inlines = [RepliesInline]

admin.site.register(Post, PostAdmin)
