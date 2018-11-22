# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-04 08:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('org_work', '0010_worksubmissions_organization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worksubmissions',
            options={'ordering': ['pub_date']},
        ),
        migrations.AddField(
            model_name='worksubmissions',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='data published'),
        ),
        migrations.AddField(
            model_name='worksubmissions',
            name='user_up_votes',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
