# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-19 07:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20181019_0756'),
        ('org_home', '0013_auto_20180727_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='positions',
            name='formal_powers',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.PowerStack'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='positions',
            name='informal_powers',
            field=models.CharField(default=3, max_length=100000),
            preserve_default=False,
        ),
    ]
