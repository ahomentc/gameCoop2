# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 19:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('org_home', '0003_auto_20180105_0540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='category_type',
            new_name='parent',
        ),
    ]
