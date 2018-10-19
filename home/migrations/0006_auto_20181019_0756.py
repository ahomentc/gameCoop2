# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-19 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20180827_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentStack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Finance', models.BooleanField(default=False)),
                ('BusinessStrategyAndDevelopment', models.BooleanField(default=False)),
                ('Accounting', models.BooleanField(default=False)),
                ('Recruiting', models.BooleanField(default=False)),
                ('ResearchAndDevelopment', models.BooleanField(default=False)),
                ('Engineering', models.BooleanField(default=False)),
                ('IT', models.BooleanField(default=False)),
                ('MarketingAndAdvertising', models.BooleanField(default=False)),
                ('Administration', models.BooleanField(default=False)),
                ('Sales', models.BooleanField(default=False)),
                ('Purchasing', models.BooleanField(default=False)),
                ('QualityAssurance', models.BooleanField(default=False)),
                ('Licenses', models.BooleanField(default=False)),
                ('CustomerAssurance', models.BooleanField(default=False)),
                ('ProductionAndInventory', models.BooleanField(default=False)),
                ('SupplyChainManagement', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PowerStack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PercentDepartmentMustVote', models.BooleanField(default=False)),
                ('AddingMembers', models.BooleanField(default=False)),
                ('RemovingMembers', models.BooleanField(default=False)),
                ('ElectionSystem', models.BooleanField(default=False)),
                ('VotingSystem', models.BooleanField(default=False)),
                ('AppointingPositions', models.BooleanField(default=False)),
                ('CreatingPositions', models.BooleanField(default=False)),
                ('AcceptingContributions', models.BooleanField(default=False)),
                ('RejectingContributions', models.BooleanField(default=False)),
                ('FinalDecisions', models.BooleanField(default=False)),
                ('ChangingMonetaryDistribution', models.BooleanField(default=False)),
                ('AssigningTasks', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='DirectDemocracy',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='AnyMember',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='AnyModOrRep',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='MemberVote',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='ModOrRepVote',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='category',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='founders',
        ),
        migrations.RemoveField(
            model_name='systemofgovernance',
            name='organization',
        ),
        migrations.DeleteModel(
            name='AnyMember',
        ),
        migrations.DeleteModel(
            name='AnyModOrRep',
        ),
        migrations.DeleteModel(
            name='MemberVote',
        ),
        migrations.DeleteModel(
            name='ModOrRepVote',
        ),
        migrations.DeleteModel(
            name='SystemOfGovernance',
        ),
    ]
