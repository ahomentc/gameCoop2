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


# Who makes what decisions
class AnyModOrRep(models.Model):
    finalProductDecisions = models.BooleanField(default=True)
    acceptingOrRejectingContribs = models.BooleanField(default=True)
    directionOfBusiness = models.BooleanField(default=False)
    removingMember = models.BooleanField(default=False)
    percentCommunityMustVote = models.BooleanField(default=False)
    numberOfMods = models.BooleanField(default=False)
    whoModsAre = models.BooleanField(default=False)
    MonetaryDistr = models.BooleanField(default=False)
    VotingSystem = models.BooleanField(default=False)
    MemberJoining = models.BooleanField(default=False)
    contributionSharesAmount = models.BooleanField(default=False)

class ModOrRepVote(models.Model):
    finalProductDecisions = models.BooleanField(default=False)
    acceptingOrRejectingContribs = models.BooleanField(default=False)
    directionOfBusiness = models.BooleanField(default=True)
    removingMember = models.BooleanField(default=True)
    percentCommunityMustVote = models.BooleanField(default=False)
    numberOfMods = models.BooleanField(default=False)
    whoModsAre = models.BooleanField(default=False)
    MonetaryDistr = models.BooleanField(default=False)
    VotingSystem = models.BooleanField(default=False)
    MemberJoining = models.BooleanField(default=False)
    contributionSharesVoting = models.BooleanField(default=False)

class AnyMember(models.Model):
    finalProductDecisions = models.BooleanField(default=False)
    acceptingOrRejectingContribs = models.BooleanField(default=False)
    directionOfBusiness = models.BooleanField(default=False)
    removingMember = models.BooleanField(default=False)
    percentCommunityMustVote = models.BooleanField(default=False)
    numberOfMods = models.BooleanField(default=False)
    whoModsAre = models.BooleanField(default=False)
    MonetaryDistr = models.BooleanField(default=False)
    VotingSystem = models.BooleanField(default=False)
    MemberJoining = models.BooleanField(default=True)
    contributionSharesVoting = models.BooleanField(default=False)

class MemberVote(models.Model):
    finalProductDecisions = models.BooleanField(default=False)
    acceptingOrRejectingContribs = models.BooleanField(default=True)
    directionOfBusiness = models.BooleanField(default=False)
    removingMember = models.BooleanField(default=False)
    percentCommunityMustVote = models.BooleanField(default=True)
    numberOfMods = models.BooleanField(default=True)
    whoModsAre = models.BooleanField(default=True)
    MonetaryDistr = models.BooleanField(default=True)
    VotingSystem = models.BooleanField(default=True)
    MemberJoining = models.BooleanField(default=False)

    # Enable users to vote on how many shares a contribution should receive
    contributionSharesVoting = models.BooleanField(default=True)

class DirectDemocracy(models.Model):
    percentCommunityMustVote = models.FloatField(default=30)
    description = models.CharField(default="Every member can vote", max_length=1000)
    organizationalJoining = models.CharField(default="MemberVote", max_length=1000)
    communityJoining = models.CharField("AnyMember", max_length=1000)
    defaultRemoving = models.CharField("MemberVote", max_length=1000)

class SystemOfGovernance(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    category = models.ForeignKey('org_home.Categories', blank=True, null=True)

    # types of governance:
    #    DirectDemocracy            Every member votes on every decision
    #    DepartmentReps             Each department elects a member to vote on their behalf for the whole of the organization
    #    MixDeptRepsDirectDem       Mix of Department Representatives and Direct Democracy... decisions can be made by either
    #    BoardOfDirectors           Multiple leaders and each department has a  person in charge
    #    OneSolDecider              One leader and each department has a person in charge
    typeFoGovernance = models.CharField(max_length=500, default='MixDeptRepsDirectDem')

    ### voting ###
    # two voting types: shareBased, and OneVotePerMember
    votingType = models.CharField(max_length=500, default='shareBased', blank=True, null=True)
    # amount of time users can vote
    votingLength = models.FloatField(default=172800) # 172800 seconds is 2 days

    # governance specific questions:

    # who makes what decisions
    AnyModOrRep = models.ForeignKey(AnyModOrRep, blank=True, null=True)
    ModOrRepVote = models.ForeignKey(ModOrRepVote, blank=True, null=True)
    AnyMember = models.ForeignKey(AnyMember, blank=True, null=True)
    MemberVote = models.ForeignKey(MemberVote, blank=True, null=True)

    founders = models.ManyToManyField(User)

    # scenarios
    userRetainSharesAfterBanishment = models.BooleanField(default=True)
    enableVestingPeriodNewMembers = models.BooleanField(default=False)      # vesting period where new member are not full
                                                                            # members until certain requirements reached
