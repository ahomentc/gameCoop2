# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
import os
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from consensusEditing.views import commitTextDocGit

from .models import Organizations
from .models import MonetaryDistribution
from org_home.models import Categories
from consensusEditing.models import TextDoc

import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
# https://github.com/ethereum/web3.py

@login_required
def IndexView(request):
    return render(request, 'home/index.html',{'member_organizations_list': Organizations.objects.filter(
        members__id=request.user.id),
    })

@login_required
def OrganizationView(request):
    return render(request,'home/organizations.html',{'organizations_list':Organizations.objects.all(),'member_organizations_list': Organizations.objects.filter(
        members__id=request.user.id),})

@login_required
def newOrganizationView(request):
    return render(request, 'home/newOrganization.html')

@login_required
def orgTypeView(request,organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    return render(request, 'home/orgType.html',{'organization':organization})

@login_required
def setMonetaryDistView(request, organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    return render(request, 'home/setMonetaryDistribution.html', {'organization': organization})

@login_required
def setGovernanceView(request, organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)
    return render(request, 'home/setGovernance.html', {'organization': organization})

@login_required
def submitNewPotentialOrg(request):
    if 'new_organization' in request.POST and request.POST['new_organization'] != '':
        # get the organization name
        organizationName = request.POST['new_organization']

        # first word in organization name uppercased
        formatedOrganizationName = ' '.join(word[0].upper() + word[1:] for word in organizationName.split())

        # returns error if the organization name already exists
        if Organizations.objects.filter(organization_name=formatedOrganizationName).exists():
            return render(request, 'home/newOrganization.html',
                          {'error_message': formatedOrganizationName + " already exists.", })

        # get the description
        description = request.POST['new_organization_desc']

        # create the organization, add the creator to the members list, and make the creator a moderator
        organization = Organizations.objects.create(organization_name=formatedOrganizationName,description=description)
        organization.members.add(request.user)
        organization.moderators.add(request.user)

        return HttpResponseRedirect(reverse('home:orgTypeView', args=(organization.id,)))

    else:
        return render(request, 'home/newOrganization.html', {
            'error_message': "Please enter a organization.",
        })

@login_required
def submitOrgType(request,organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)

    if 'org_type' in request.POST:
        organization.organization_type = request.POST['org_type']
        return HttpResponseRedirect(reverse('home:setMonetaryDistView', args=(organization.id,)))
    else:
        return render(request, 'home/orgType.html', {'organization': organization,
                                                     'error_message':'Please select a type of organization'})


@login_required
def submitMonetaryDist(request, organization_id):
    organization = get_object_or_404(Organizations, id=organization_id)

    monetaryDist = MonetaryDistribution.objects.create(organization=organization)

    if 'iwfPercent' in request.POST:
        monetaryDist.InvestorsWorkersFounders = request.POST['iwfPercent']

    if 'orgBankPercent' in request.POST:
        monetaryDist.OrgBank = request.POST['orgBankPercent']

    if 'sharesPerDollar' in request.POST:
        monetaryDist.sharesPerDollarInvested = request.POST['sharesPerDollar']

    if 'sharesPerForumUpvote' in request.POST:
        monetaryDist.sharesPerUpvoteOnForumPost = request.POST['sharesPerForumUpvote']

    if 'sharesPerContribUpvote' in request.POST:
        monetaryDist.sharesPerUpvoteOnContribution = request.POST['sharesPerContribUpvote']

    if 'sharesPerAcceptedIdea' in request.POST:
        monetaryDist.sharesPerAcceptedPostedIdea = request.POST['sharesPerAcceptedIdea']

    if 'baseNumberSharesUsedContrib' in request.POST:
        monetaryDist.sharesPerUsedContrib = request.POST['baseNumberSharesUsedContrib']

    if 'initialFounderNum' in request.POST:
        monetaryDist.numOriginalFounders = request.POST['initialFounderNum']

    if 'initialFounderBonus' in request.POST:
        monetaryDist.sharesPerFounderBonus = request.POST['initialFounderBonus']

    if 'codeUseReward' in request.POST:
        monetaryDist.sharesPerEachUseOfCode = request.POST['codeUseReward']

    if 'SharesPerLine' in request.POST:
        monetaryDist.sharesPerLineAcceptedCode = request.POST['SharesPerLine']

    if 'machine_learning_distr' in request.POST:
        if request.POST['machine_learning_distr'] == 'true':
            monetaryDist.machineLearningShareDistr = True
        elif request.POST['machine_learning_distr'] == 'false':
            monetaryDist.machineLearningShareDistr = False

    monetaryDist.save()

    return HttpResponseRedirect(reverse('home:setGovernanceView', args=(organization.id,)))

# submit creation of a new organization
@login_required
def submitNewOrganization(request):
    if 'new_organization' in request.POST and request.POST['new_organization'] != '':
        closedOrganization = False
        gate_keeper = ''
        # close_organization is a checkbox of if people need persmission to join the category
        if 'closed_organization' in request.POST:
            closedOrganization = True
            # gate_keeper is who can let people join the community. It can either be anyone in the community
            # or the moderator. access is the name of the radio field
            gate_keeper = request.POST['access']

        organizationName =  request.POST['new_organization']
        # first word in organization name uppercased
        formatedOrganizationName = ' '.join(word[0].upper() + word[1:] for word in organizationName.split())

        # returns error if the organization name already exists
        if Organizations.objects.filter(organization_name=formatedOrganizationName).exists():
            return render(request, 'home/newOrganization.html', {'error_message': formatedOrganizationName + " already exists.",})

        new_organization_desc = ""
        if "new_organization_desc" in request.POST:
            new_organization_desc = request.POST['new_organization_desc']

        # create and deploy an Org smart contract 
        w3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))

        abiJson = """ [ { "constant": false, "inputs": [ { "name": "userId", "type": "uint256" }, { "name": "userAddress", "type": "address" } ], "name": "addUserAddress", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "getBal", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "percentage", "type": "uint256" } ], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "userIds", "type": "uint256[]" }, { "name": "userPercentages", "type": "uint256[]" } ], "name": "distributeToMultiple", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "userId", "type": "uint256" }, { "name": "percentage", "type": "uint256" } ], "name": "distributeToIndividual", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" } ] """
        # bytecodeJson = """ { "linkReferences": {}, "object": "608060405234801561001057600080fd5b506105a1806100206000396000f3fe608060405260043610610072576000357c0100000000000000000000000000000000000000000000000000000000900480631be5879a1461007757806325caa262146100d25780632e1a7d4d146100fd5780633855a0b214610138578063d0e30db014610291578063f9432dee1461029b575b600080fd5b34801561008357600080fd5b506100d06004803603604081101561009a57600080fd5b8101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506102e0565b005b3480156100de57600080fd5b506100e7610335565b6040518082815260200191505060405180910390f35b34801561010957600080fd5b506101366004803603602081101561012057600080fd5b8101908080359060200190929190505050610354565b005b34801561014457600080fd5b5061028f6004803603604081101561015b57600080fd5b810190808035906020019064010000000081111561017857600080fd5b82018360208201111561018a57600080fd5b803590602001918460208302840111640100000000831117156101ac57600080fd5b919080806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561020c57600080fd5b82018360208201111561021e57600080fd5b8035906020019184602083028401116401000000008311171561024057600080fd5b919080806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505091929192905050506103d2565b005b6102996104d1565b005b3480156102a757600080fd5b506102de600480360360408110156102be57600080fd5b8101908080359060200190929190803590602001909291905050506104d3565b005b8060008084815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050565b60003073ffffffffffffffffffffffffffffffffffffffff1631905090565b600061035e610335565b905060008111151561036f57600080fd5b600061271083606484020281151561038357fe5b0490503373ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f193505050501580156103cc573d6000803e3d6000fd5b50505050565b60006103dc610335565b905060008090505b83518110156104cb57600084828151811015156103fd57fe5b9060200190602002015190506000848381518110151561041957fe5b906020019060200201519050600061271082606487020281151561043957fe5b049050600080600085815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff166108fc839081150290604051600060405180830381858888f193505050501580156104b9573d6000803e3d6000fd5b505050505080806001019150506103e4565b50505050565b565b60006127108260646104e3610335565b02028115156104ee57fe5b049050600080600085815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff166108fc839081150290604051600060405180830381858888f1935050505015801561056e573d6000803e3d6000fd5b505050505056fea165627a7a723058208ea2035b5326f21c14cd452afbbcef81774b9526fd49879aadefccf1d6b570450029", "opcodes": "PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH2 0x10 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x5A1 DUP1 PUSH2 0x20 PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN INVALID PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH2 0x72 JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV DUP1 PUSH4 0x1BE5879A EQ PUSH2 0x77 JUMPI DUP1 PUSH4 0x25CAA262 EQ PUSH2 0xD2 JUMPI DUP1 PUSH4 0x2E1A7D4D EQ PUSH2 0xFD JUMPI DUP1 PUSH4 0x3855A0B2 EQ PUSH2 0x138 JUMPI DUP1 PUSH4 0xD0E30DB0 EQ PUSH2 0x291 JUMPI DUP1 PUSH4 0xF9432DEE EQ PUSH2 0x29B JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x83 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0xD0 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x40 DUP2 LT ISZERO PUSH2 0x9A JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 SWAP3 SWAP2 SWAP1 DUP1 CALLDATALOAD PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SWAP1 PUSH1 0x20 ADD SWAP1 SWAP3 SWAP2 SWAP1 POP POP POP PUSH2 0x2E0 JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0xDE JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0xE7 PUSH2 0x335 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP3 DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x109 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x136 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x20 DUP2 LT ISZERO PUSH2 0x120 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 SWAP3 SWAP2 SWAP1 POP POP POP PUSH2 0x354 JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x144 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x28F PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x40 DUP2 LT ISZERO PUSH2 0x15B JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x178 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x18A JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x1AC JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP2 SWAP1 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP SWAP2 SWAP3 SWAP2 SWAP3 SWAP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x20C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x21E JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x240 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP2 SWAP1 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP SWAP2 SWAP3 SWAP2 SWAP3 SWAP1 POP POP POP PUSH2 0x3D2 JUMP JUMPDEST STOP JUMPDEST PUSH2 0x299 PUSH2 0x4D1 JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x2A7 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x2DE PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x40 DUP2 LT ISZERO PUSH2 0x2BE JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 SWAP3 SWAP2 SWAP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 SWAP3 SWAP2 SWAP1 POP POP POP PUSH2 0x4D3 JUMP JUMPDEST STOP JUMPDEST DUP1 PUSH1 0x0 DUP1 DUP5 DUP2 MSTORE PUSH1 0x20 ADD SWAP1 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x0 KECCAK256 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF MUL NOT AND SWAP1 DUP4 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND MUL OR SWAP1 SSTORE POP POP POP JUMP JUMPDEST PUSH1 0x0 ADDRESS PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND BALANCE SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH2 0x35E PUSH2 0x335 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP2 GT ISZERO ISZERO PUSH2 0x36F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 PUSH2 0x2710 DUP4 PUSH1 0x64 DUP5 MUL MUL DUP2 ISZERO ISZERO PUSH2 0x383 JUMPI INVALID JUMPDEST DIV SWAP1 POP CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x8FC DUP3 SWAP1 DUP2 ISZERO MUL SWAP1 PUSH1 0x40 MLOAD PUSH1 0x0 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP6 DUP9 DUP9 CALL SWAP4 POP POP POP POP ISZERO DUP1 ISZERO PUSH2 0x3CC JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3DC PUSH2 0x335 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST DUP4 MLOAD DUP2 LT ISZERO PUSH2 0x4CB JUMPI PUSH1 0x0 DUP5 DUP3 DUP2 MLOAD DUP2 LT ISZERO ISZERO PUSH2 0x3FD JUMPI INVALID JUMPDEST SWAP1 PUSH1 0x20 ADD SWAP1 PUSH1 0x20 MUL ADD MLOAD SWAP1 POP PUSH1 0x0 DUP5 DUP4 DUP2 MLOAD DUP2 LT ISZERO ISZERO PUSH2 0x419 JUMPI INVALID JUMPDEST SWAP1 PUSH1 0x20 ADD SWAP1 PUSH1 0x20 MUL ADD MLOAD SWAP1 POP PUSH1 0x0 PUSH2 0x2710 DUP3 PUSH1 0x64 DUP8 MUL MUL DUP2 ISZERO ISZERO PUSH2 0x439 JUMPI INVALID JUMPDEST DIV SWAP1 POP PUSH1 0x0 DUP1 PUSH1 0x0 DUP6 DUP2 MSTORE PUSH1 0x20 ADD SWAP1 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x0 KECCAK256 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SWAP1 POP DUP1 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x8FC DUP4 SWAP1 DUP2 ISZERO MUL SWAP1 PUSH1 0x40 MLOAD PUSH1 0x0 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP6 DUP9 DUP9 CALL SWAP4 POP POP POP POP ISZERO DUP1 ISZERO PUSH2 0x4B9 JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP POP POP DUP1 DUP1 PUSH1 0x1 ADD SWAP2 POP POP PUSH2 0x3E4 JUMP JUMPDEST POP POP POP POP JUMP JUMPDEST JUMP JUMPDEST PUSH1 0x0 PUSH2 0x2710 DUP3 PUSH1 0x64 PUSH2 0x4E3 PUSH2 0x335 JUMP JUMPDEST MUL MUL DUP2 ISZERO ISZERO PUSH2 0x4EE JUMPI INVALID JUMPDEST DIV SWAP1 POP PUSH1 0x0 DUP1 PUSH1 0x0 DUP6 DUP2 MSTORE PUSH1 0x20 ADD SWAP1 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x0 KECCAK256 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SWAP1 POP DUP1 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x8FC DUP4 SWAP1 DUP2 ISZERO MUL SWAP1 PUSH1 0x40 MLOAD PUSH1 0x0 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP6 DUP9 DUP9 CALL SWAP4 POP POP POP POP ISZERO DUP1 ISZERO PUSH2 0x56E JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP POP POP JUMP INVALID LOG1 PUSH6 0x627A7A723058 KECCAK256 DUP15 LOG2 SUB JUMPDEST MSTORE8 0x26 CALLCODE SHR EQ 0xcd GASLIMIT 0x2a 0xfb 0xbc 0xef DUP2 PUSH24 0x4B9526FD49879AADEFCCF1D6B57045002900000000000000 ", "sourceMap": "25:2004:0:-;;;;8:9:-1;5:2;;;30:1;27;20:12;5:2;25:2004:0;;;;;;;" } """

        contract = w3.eth.contract(abi=json.loads(abiJson),bytecode="608060405234801561001057600080fd5b506105a1806100206000396000f3fe608060405260043610610072576000357c0100000000000000000000000000000000000000000000000000000000900480631be5879a1461007757806325caa262146100d25780632e1a7d4d146100fd5780633855a0b214610138578063d0e30db014610291578063f9432dee1461029b575b600080fd5b34801561008357600080fd5b506100d06004803603604081101561009a57600080fd5b8101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506102e0565b005b3480156100de57600080fd5b506100e7610335565b6040518082815260200191505060405180910390f35b34801561010957600080fd5b506101366004803603602081101561012057600080fd5b8101908080359060200190929190505050610354565b005b34801561014457600080fd5b5061028f6004803603604081101561015b57600080fd5b810190808035906020019064010000000081111561017857600080fd5b82018360208201111561018a57600080fd5b803590602001918460208302840111640100000000831117156101ac57600080fd5b919080806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561020c57600080fd5b82018360208201111561021e57600080fd5b8035906020019184602083028401116401000000008311171561024057600080fd5b919080806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505091929192905050506103d2565b005b6102996104d1565b005b3480156102a757600080fd5b506102de600480360360408110156102be57600080fd5b8101908080359060200190929190803590602001909291905050506104d3565b005b8060008084815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050565b60003073ffffffffffffffffffffffffffffffffffffffff1631905090565b600061035e610335565b905060008111151561036f57600080fd5b600061271083606484020281151561038357fe5b0490503373ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f193505050501580156103cc573d6000803e3d6000fd5b50505050565b60006103dc610335565b905060008090505b83518110156104cb57600084828151811015156103fd57fe5b9060200190602002015190506000848381518110151561041957fe5b906020019060200201519050600061271082606487020281151561043957fe5b049050600080600085815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff166108fc839081150290604051600060405180830381858888f193505050501580156104b9573d6000803e3d6000fd5b505050505080806001019150506103e4565b50505050565b565b60006127108260646104e3610335565b02028115156104ee57fe5b049050600080600085815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff166108fc839081150290604051600060405180830381858888f1935050505015801561056e573d6000803e3d6000fd5b505050505056fea165627a7a723058208ea2035b5326f21c14cd452afbbcef81774b9526fd49879aadefccf1d6b570450029")

        # pwd = os.path.dirname(__file__)
        # contract_file = open(pwd + '/Org.sol')
        # compiled_sol = compile_source(contract_file.read())
        # contract_interface = compiled_sol['<stdin>:Greeter']
        # contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0]})
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress']

        print("contract address:")
        print(contract_address)

        # create the organization, add the creator to the members list, and make the creator a moderator
        organization = Organizations.objects.create(organization_name=formatedOrganizationName,description=new_organization_desc, closed_organization=closedOrganization, gateKeeper=gate_keeper, contract_address=contract_address)
        organization.members.add(request.user)
        organization.moderators.add(request.user)

        # auto create executive category
        category = Categories.objects.create(organization=organization,parent=None,category_name="Executive",closed_category = True, gateKeeper="moderators",needAcceptedContribs=True)
        category.members.add(request.user)
        category.moderators.add(request.user)
        #
        # # create file system for organization and git
        # organization.save()
        # CreateOrgFiles(organization.pk)
        # CreateOrgBaseFiles(organization.pk)

        return HttpResponseRedirect(reverse('home:organizations'))
    else:
        return render(request, 'home/newOrganization.html', {
            'error_message': "Please enter a organization.",
        })
