# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-31 08:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org_home', '0006_categories_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org_home.Categories'),
        ),
    ]
