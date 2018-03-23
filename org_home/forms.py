from django import forms
from .models import Categories
from home.models import Organizations
from django.shortcuts import get_object_or_404

class ParentCategories(forms.Form):
    parent_branch = forms.ChoiceField(choices = [])
