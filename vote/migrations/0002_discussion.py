# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-13 03:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(blank=True, null=True, verbose_name='data published')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vote.Discussion')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.Question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('userDownVotes', models.ManyToManyField(blank=True, related_name='DecisionDownVotes', to=settings.AUTH_USER_MODEL)),
                ('userUpVotes', models.ManyToManyField(blank=True, related_name='DecisionUpVotes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
    ]