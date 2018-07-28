# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-29 02:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('org_work', '0007_auto_20180501_0638'),
        ('org_home', '0009_auto_20180428_0820'),
        ('consensusEditing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textdoc',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org_home.Categories'),
        ),
        migrations.AddField(
            model_name='textdoc',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Organizations'),
        ),
        migrations.AddField(
            model_name='textdoc',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org_work.Projects'),
        ),
    ]
