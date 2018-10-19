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
    PercentDepartmentMustVote = models.BooleanField()
    AddingMembers = models.BooleanField()
    RemovingMembers = models.BooleanField()
    ElectionSystem = models.BooleanField()
    VotingSystem = models.BooleanField()
    AppointingPositions = models.BooleanField()
    CreatingPositions = models.BooleanField()
    AcceptingContributions = models.BooleanField()
    RejectingContributions = models.BooleanField()
    FinalDecisions = models.BooleanField()
    ChangingMonetaryDistribution = models.BooleanField()
    AssigningTasks = models.BooleanField()

class DepartmentStack(models.Model):
    Finance = models.BooleanField()
    BusinessStrategyAndDevelopment = models.BooleanField()
    Accounting = models.BooleanField()
    Recruiting = models.BooleanField()
    ResearchAndDevelopment = models.BooleanField()
    Engineering = models.BooleanField()
    IT = models.BooleanField()
    MarketingAndAdvertising = models.BooleanField()
    Administration = models.BooleanField()
    Sales = models.BooleanField()
    Purchasing = models.BooleanField()
    QualityAssurance = models.BooleanField()
    Licenses = models.BooleanField()
    CustomerAssurance = models.BooleanField()
    ProductionAndInventory = models.BooleanField()
    SupplyChainManagement = models.BooleanField()

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
    doElectionsOccur = models.BooleanField()
    frequencyOfElections = models.IntegerField()
    maxNumberReElections = models.IntegerField()

    # Super Member Criteria
    minNumberMemberDays = models.IntegerField()
    minNumberShares = models.IntegerField()
    minNumberAcceptedContribs = models.IntegerField()
    votedIn = models.BooleanField()
    acceptedByAuthority = models.BooleanField()

    # founders
    founders = models.ManyToManyField(User)

    # scenarios
    userRetainSharesAfterBanishment = models.BooleanField(default=True)
