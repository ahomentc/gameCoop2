# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-01 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org_work', '0006_auto_20180428_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relatedParent', to='org_work.Projects'),
        ),
    ]