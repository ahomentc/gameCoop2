# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.urls import reverse
from django.utils import timezone
from org_home import models as org_home_models
from django.contrib.auth.decorators import login_required


from org_home.models import Categories
from home.models import Organizations
from .models import Post,Reply
from .forms import newPost,newMainReply

# decorator that checks if user is a member of the category
def is_member(func):
    def check(request,*args, **kwargs):
        if 'category_id' in kwargs:
            category = get_object_or_404(org_home_models.Categories,pk=kwargs['category_id'])
        if 'organization_id' in kwargs:
            organization = get_object_or_404(Organizations,pk=kwargs['organization_id'])
        try:
            if request.user in category.members.all():
                return func(request,*args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,category.id,)))
        except:
            return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,category.id,)))
    check.__doc__=func.__doc__
    check.__name__=func.__name__
    return check

@is_member
@login_required
# org_home page of discussion. Show the "general" discussion.
def Index(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    no_posts_message = ''
    generalPostsList = Post.objects.filter(
            category=category,
            discussionType='General'
        ).order_by('-pub_date')[:10]
    if len(generalPostsList) == 0:
        no_posts_message = "No posts here yet"
    return render(request,'discuss/index.html',{'organization':organization,'category': category,'postsList':generalPostsList,'no_posts_message':no_posts_message,
                                                'categories_list':Categories.objects.filter(organization=organization)})
@is_member
@login_required
# the "idea" discussions
def IdeaDiscussion(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    no_posts_message = ''
    ideaPostsList = Post.objects.filter(
            category=category,
            discussionType='Idea'
        ).order_by('-pub_date')[:10]
    if len(ideaPostsList) == 0:
        no_posts_message = "No posts here yet"
    return render(request,'discuss/ideaDiscussion.html',{'organization':organization,'category': category,'postsList':ideaPostsList,'no_posts_message':no_posts_message,
                                                         'categories_list':Categories.objects.filter(organization=organization)})
@is_member
@login_required
# the "voting" discussion
def VotingDiscussion(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    no_posts_message = ''
    votingPostsList = Post.objects.filter(
            category=category,
            discussionType='Voting'
        ).order_by('-pub_date')[:10]
    if len(votingPostsList) == 0:
        no_posts_message = "No posts here yet"
    return render(request,'discuss/ideaDiscussion.html',{'organization':organization,'category': category,'postsList':votingPostsList,'no_posts_message':no_posts_message,
                                                         'categories_list':Categories.objects.filter(organization=organization)})
@is_member
@login_required
# page to create a new Post
def newPostView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)

    form = newPost()
    return render(request,'discuss/newPost.html',{'organization':organization,'category':category,'form':form})

@is_member
@login_required
# submit that post
def submitNewPost(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    if request.method == "POST":
        form = newPost(request.POST)
        if form.is_valid():
            discussionType = request.POST['discussionType']
            Post.objects.create(
                discussionType=discussionType,
                category=category,
                title=request.POST['title'],
                content=request.POST['content'],
                pub_date=timezone.now(),
                original_poster=request.user
            )
            # go to the page that the post was created for
            if discussionType == 'Idea':
                return HttpResponseRedirect(reverse('discuss:IdeaDiscussion', args=(organization.id,category.id)))
            elif discussionType == 'Voting':
                return HttpResponseRedirect(reverse('discuss:VotingDiscussion', args=(organization.id,category.id)))
            else:
                return HttpResponseRedirect(reverse('discuss:Index', args=(organization.id,category.id)))
    else:
        form = newPost()
    return render(request,'discuss/newPost.html',{'organization':organization,'category':category,'form':form})

# recursively get an infinitely nested dictionary of all the replies
def getRepliesNestedDict(highestList,post):
    tempDict = {}
    for element in highestList:
        subReplies = Reply.objects.filter(post=post,parent=element)
        if len(subReplies) == 0:
            tempDict[element] = None
        else:
            tempDict[element] = getRepliesNestedDict(subReplies,post)
    return tempDict

# returns a dictionary where the subdictionaries have been flattened to a list
def correctlyFormatDict(dict):
    newDict = {}
    for key,value in dict.items():
        if value is None:
            newDict[key] = None
        else:
            newDict[key] = sorted(flattenDict(value),key=lambda x:x.pub_date,reverse=False)
    return newDict

# recursively flattens a dictionary that looks like this: {a:{b:None,c:{d:None}},e:None} to a list [a,b,c,d,e]
def flattenDict(dict):
    tempList = []
    for key,value in dict.items():
        tempList = tempList + [key]
        if value != None:
            tempList = tempList + flattenDict(value)
    return tempList

def getRepliesUserLiked(post,user):
    allReplies = Reply.objects.filter(post=post)
    replies = []
    for reply in allReplies:
        if user in reply.userUpVotes.all():
            replies.append(reply)
    return replies

def getRepliesUserDisliked(post,user):
    allReplies = Reply.objects.filter(post=post)
    replies = []
    for reply in allReplies:
        if user in reply.userDownVotes.all():
            replies.append(reply)
    return replies

@is_member
@login_required
# shows an individual post and all the replies to it
def IndividualPost(request,organization_id,category_id,post_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    post = get_object_or_404(Post,pk=post_id)

    # list of replies that are not replies to a reply to the post
    noParentsList = Reply.objects.filter(post=post,parent__isnull=True).order_by('-pub_date')
    # dictionary with    keys: noParentsList items   values: list of all the replies to each key
    sortedDict = {}
    repliesDict = correctlyFormatDict(getRepliesNestedDict(noParentsList,post))
    for key in sorted(repliesDict.keys(),key=lambda x: x.pub_date):
        sortedDict[key] = repliesDict[key]

    repliesUserLiked = getRepliesUserLiked(post,request.user)
    repliesUserDisliked = getRepliesUserDisliked(post, request.user)

    userLikedPost = request.user in post.userUpVotes.all()
    userDislikedPost = request.user in post.userDownVotes.all()

    form = newMainReply()
    return render(request,'discuss/individualPost.html',{'organization':organization,'category':category,'post':post,'form':form,'repliesDict':sortedDict,
                                                         'categories_list':Categories.objects.filter(organization=organization),
                                                         'repliesUserLiked':repliesUserLiked,
                                                         'repliesUserDisliked': repliesUserDisliked,
                                                         'userLikedPost':userLikedPost,
                                                         'userDislikedPost':userDislikedPost})

@is_member
@login_required
# submit a reply
def submitReply(request,organization_id,category_id,post_id,parent_id=None):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    post = get_object_or_404(Post,pk=post_id)

    # parent id is optional
    if parent_id is not None:
        parent = get_object_or_404(Reply,pk=parent_id)
    else:
        parent=None
    if request.method == "POST":
        form = newMainReply(request.POST)
        if form.is_valid():
            r = Reply.objects.create(
                post=post,
                parent=parent,
                content=request.POST['content'],
                user=request.user,
                pub_date=timezone.now()
            )
            return HttpResponseRedirect(reverse('discuss:IndividualPost', args=(organization.id,category.id,post.id)))
    else:
        form = newMainReply()
    return render(request,'discuss/individualPost.html',{'organization':organization,'category':category,'post':post,'form':form})


@is_member
@login_required
# edit a reply
def editReply(request,organization_id,category_id,post_id,reply_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    post = get_object_or_404(Post,pk=post_id)

    if request.method == "POST":
        form = newMainReply(request.POST)
        print(request.POST)
        for c in request.POST:
            if '_editTextbox' in c:
                obj = get_object_or_404(Reply,id=reply_id)
                obj.content = request.POST[c]
                obj.save()
        return HttpResponseRedirect(reverse('discuss:IndividualPost', args=(organization.id, category.id, post.id)))
    else:
        form = newMainReply()
    return render(request, 'discuss/individualPost.html',
                  {'organization': organization, 'category': category, 'post': post, 'form': form})

@is_member
@login_required
# edit a reply
def deleteReply(request,organization_id,category_id,post_id,reply_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    post = get_object_or_404(Post,pk=post_id)
    reply = get_object_or_404(Reply,id=reply_id)
    reply.content = '[deleted]'
    reply.save()
    form = newMainReply(request.POST)
    return HttpResponseRedirect(reverse('discuss:IndividualPost', args=(organization.id, category.id, post.id)))


#vote for a reply
def voteForReply(request):
    reply_id = int(request.POST.get('id'))
    vote_type = request.POST.get('type')
    vote_action = request.POST.get('action')

    reply = get_object_or_404(Reply, pk=reply_id)

    thisUserUpVote = reply.userUpVotes.filter(id = request.user.id).count()
    thisUserDownVote = reply.userDownVotes.filter(id = request.user.id).count()

    if (vote_action == 'vote'):
        if(vote_type == 'up' and thisUserUpVote == 0):
            if(thisUserDownVote == 1):
                reply.userDownVotes.remove(request.user)
            reply.userUpVotes.add(request.user)
        elif(vote_type == 'down' and thisUserDownVote == 0):
            if(thisUserUpVote == 1):
                reply.userUpVotes.remove(request.user)
            reply.userDownVotes.add(request.user)
        else:
            return HttpResponse('error - already voted')
    elif (vote_action == 'recall-vote'):
        if (vote_type == 'up') and (thisUserUpVote == 1):
            reply.userUpVotes.remove(request.user)
        elif (vote_type == 'down') and (thisUserDownVote ==1):
            reply.userDownVotes.remove(request.user)
        else:
            return HttpResponse('error - unknown vote type or no vote to recall')
    else:
        return HttpResponse('error - bad action')
    num_votes = reply.userUpVotes.count() - reply.userDownVotes.count()
    return HttpResponse(num_votes)

#vote for a post
def voteForPost(request):
    post_id = int(request.POST.get('id'))
    vote_type = request.POST.get('type')
    vote_action = request.POST.get('action')

    post = get_object_or_404(Post, pk=post_id)

    thisUserUpVote = post.userUpVotes.filter(id = request.user.id).count()
    thisUserDownVote = post.userDownVotes.filter(id = request.user.id).count()

    if (vote_action == 'vote'):
        if(vote_type == 'up' and thisUserUpVote == 0):
            if(thisUserDownVote == 1):
                post.userDownVotes.remove(request.user)
            post.userUpVotes.add(request.user)
        elif(vote_type == 'down' and thisUserDownVote == 0):
            if(thisUserUpVote == 1):
                post.userUpVotes.remove(request.user)
            post.userDownVotes.add(request.user)
        else:
            return HttpResponse('error - already voted')
    elif (vote_action == 'recall-vote'):
        if (vote_type == 'up') and (thisUserUpVote == 1):
            post.userUpVotes.remove(request.user)
        elif (vote_type == 'down') and (thisUserDownVote ==1):
            post.userDownVotes.remove(request.user)
        else:
            return HttpResponse('error - unknown vote type or no vote to recall')
    else:
        return HttpResponse('error - bad action')
    num_votes = post.userUpVotes.count() - post.userDownVotes.count()
    return HttpResponse(num_votes)

