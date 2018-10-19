# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Organizations(models.Model):
    organization_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='')

    organization_type = models.CharField(max_length=100, default='')

    pending_members = models.ManyToManyField(User,related_name='organization_pending_member')
    members = models.ManyToManyField(User,related_name='organization_member')
    moderators = models.ManyToManyField(User,related_name='organization_super_member')

    closed_organization = models.BooleanField(default=False)
    gateKeeper = models.CharField(max_length=30, default='') # either all_members or moderators

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.organization_name

class MonetaryDistribution(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)

    # Profit Partitions
    InvestorsWorkersFounders = models.FloatField(default=80)
    OrgBank = models.FloatField(default=14)
    ServiceFee = models.FloatField(default=6)

    # Investment
    sharesPerDollarInvested = models.FloatField(default=100)

    # Contributing
    sharesPerUpvoteOnForumPost = models.FloatField(default=0)
    sharesPerUpvoteOnContribution = models.FloatField(default=10)
    sharesPerAcceptedPostedIdea = models.FloatField(default=100)
    sharesPerUsedContrib = models.FloatField(default=100)

    # Founder bonus
    numOriginalFounders = models.FloatField(default=10)
    sharesPerFounderBonus = models.FloatField(default=100000)

    # Code contributions
    sharesPerEachUseOfCode = models.FloatField(default=50)
    sharesPerLineAcceptedCode = models.FloatField(default=100)

    # Enable the use of machine learning of learn how valuable contribuitons are and reward based on model
    machineLearningShareDistr = models.BooleanField(default=False)


class PowerStack(models.Model):
    PercentDepartmentMustVote = models.BooleanField(default=False)
    AddingMembers = models.BooleanField(default=False)
    RemovingMembers = models.BooleanField(default=False)
    ElectionSystem = models.BooleanField(default=False)
    VotingSystem = models.BooleanField(default=False)
    AppointingPositions = models.BooleanField(default=False)
    CreatingPositions = models.BooleanField(default=False)
    AcceptingContributions = models.BooleanField(default=False)
    RejectingContributions = models.BooleanField(default=False)
    FinalDecisions = models.BooleanField(default=False)
    ChangingMonetaryDistribution = models.BooleanField(default=False)
    AssigningTasks = models.BooleanField(default=False)

class DepartmentStack(models.Model):
    Finance = models.BooleanField(default=False)
    BusinessStrategyAndDevelopment = models.BooleanField(default=False)
    Accounting = models.BooleanField(default=False)
    Recruiting = models.BooleanField(default=False)
    ResearchAndDevelopment = models.BooleanField(default=False)
    Engineering = models.BooleanField(default=False)
    IT = models.BooleanField(default=False)
    MarketingAndAdvertising = models.BooleanField(default=False)
    Administration = models.BooleanField(default=False)
    Sales = models.BooleanField(default=False)
    Purchasing = models.BooleanField(default=False)
    QualityAssurance = models.BooleanField(default=False)
    Licenses = models.BooleanField(default=False)
    CustomerAssurance = models.BooleanField(default=False)
    ProductionAndInventory = models.BooleanField(default=False)
    SupplyChainManagement = models.BooleanField(default=False)

class SystemOfGovernance(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    category = models.ForeignKey('org_home.Categories', blank=True, null=True)

    # types of governance:
    #    DirectDemocracy
    #    DepartmentReps
    #    Hierarchical
    typeFoGovernance = models.CharField(max_length=500, default='MixDeptRepsDirectDem')

    # Departments organization has:
    departments = models.ForeignKey(DepartmentStack)

    # Voting System in Departments: two voting types: shareBased, and OneVotePerMember
    votingType = models.CharField(max_length=500, default='shareBased', blank=True, null=True)
    votingLength = models.FloatField(default=172800) # 172800 seconds is 2 days             # amount of time users can vote

    # Election System in Departments:
    doElectionsOccur = models.BooleanField(default=False)
    frequencyOfElections = models.IntegerField(default=0)
    maxNumberReElections = models.IntegerField(default=0)

    # Super Member Criteria
    minNumberMemberDays = models.IntegerField(default=0)
    minNumberShares = models.IntegerField(default=0)
    minNumberAcceptedContribs = models.IntegerField(default=0)
    votedIn = models.BooleanField(default=False)
    acceptedByAuthority = models.BooleanField(default=False)

    # founders
    founders = models.ManyToManyField(User)

    # scenarios
    userRetainSharesAfterBanishment = models.BooleanField(default=True)
