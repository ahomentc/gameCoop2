from django import forms

class NewProjectForm(forms.Form):
    project_name = forms.CharField(max_length=30, label='Project Name')
