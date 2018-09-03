# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-27 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_anymember_anymodorrep_membervote_modorrepvote_monetarydistribution_systemofgovernance'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectDemocracy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentCommunityMustVote', models.FloatField(default=30)),
                ('description', models.CharField(default='Every member can vote', max_length=1000)),
                ('organizationalJoining', models.CharField(default='MemberVote', max_length=1000)),
                ('communityJoining', models.CharField(max_length=1000, verbose_name='AnyMember')),
                ('defaultRemoving', models.CharField(max_length=1000, verbose_name='MemberVote')),
            ],
        ),
        migrations.RemoveField(
            model_name='monetarydistribution',
            name='contribVoteLength',
        ),
        migrations.RemoveField(
            model_name='monetarydistribution',
            name='contributionSharesVotable',
        ),
        migrations.RemoveField(
            model_name='monetarydistribution',
            name='numVoteForContrib',
        ),
        migrations.AddField(
            model_name='anymember',
            name='contributionSharesVoting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='anymodorrep',
            name='contributionSharesAmount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membervote',
            name='contributionSharesVoting',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='modorrepvote',
            name='contributionSharesVoting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='systemofgovernance',
            name='votingLength',
            field=models.FloatField(default=172800),
        ),
        migrations.AlterField(
            model_name='systemofgovernance',
            name='AnyMember',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.AnyMember'),
        ),
        migrations.AlterField(
            model_name='systemofgovernance',
            name='AnyModOrRep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.AnyModOrRep'),
        ),
        migrations.AlterField(
            model_name='systemofgovernance',
            name='MemberVote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.MemberVote'),
        ),
        migrations.AlterField(
            model_name='systemofgovernance',
            name='ModOrRepVote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.ModOrRepVote'),
        ),
    ]
