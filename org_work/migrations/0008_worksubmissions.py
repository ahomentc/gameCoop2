# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-19 07:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org_work', '0007_auto_20180501_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkSubmissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=1000)),
                ('linkToSubmission', models.CharField(default='', max_length=1000)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org_work.Projects')),
            ],
        ),
    ]
