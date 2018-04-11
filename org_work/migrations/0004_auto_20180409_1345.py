# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-09 13:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org_home', '0008_remove_categories_projects'),
        ('home', '0001_initial'),
        ('org_work', '0003_auto_20180331_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org_home.Categories'),
        ),
        migrations.AddField(
            model_name='projects',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Organizations'),
        ),
        migrations.AddField(
            model_name='projects',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org_work.Projects'),
        ),
    ]
