# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic,View
from django.db.models import F
from django.utils import timezone
from django.forms.formsets import formset_factory
from org_home import models as org_home_models
from django.contrib.auth.decorators import login_required

from .models import Choice, Question
from org_home.models import Categories
from home.models import Organizations
from discuss.models import Post

from discuss.forms import newMainReply
from discuss.RepliesHelper import ReplyHelper

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


# page with all the polls being voted on in the community
@is_member
@login_required
def IndexView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(org_home_models.Categories,pk=category_id)
    return render(request,'vote/index.html',{
        'organization':organization,
        'category': category,
        'latest_question_list': Question.objects.filter(
            pub_date__lte=timezone.now(),category = category
        ).order_by('-pub_date')[:5],
        'categories_list':Categories.objects.filter(organization=organization)
    })

# shows the options to vote on for a specific poll. Can vote here too.
@is_member
@login_required
def DetailView(request,organization_id,category_id,question_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(org_home_models.Categories,pk=category_id)
    question = get_object_or_404(Question,pk=question_id)
    post = question.post

    replyHelper = ReplyHelper(post, request.user)
    sortedDict = replyHelper.getSortedDict()

    repliesUserLiked = replyHelper.getRepliesUserLiked()
    repliesUserDisliked = replyHelper.getRepliesUserDisliked()

    userLikedPost = request.user in post.userUpVotes.all()
    userDislikedPost = request.user in post.userDownVotes.all()

    form = newMainReply()

    return render(request,'vote/detail.html',{
        'organization':organization,
        'category': category,
        'question':question,
        'post': post,
        'choice_set':Question.objects.filter(pub_date__lte=timezone.now()),
        'categories_list':Categories.objects.filter(organization=organization),
        'form': form, 'repliesDict': sortedDict,
        'repliesUserLiked': repliesUserLiked,
        'repliesUserDisliked': repliesUserDisliked,
        'userLikedPost': userLikedPost,
        'userDislikedPost': userDislikedPost
    })

# shows the results of the vote so far
@is_member
@login_required
def ResultsView(request,organization_id,category_id,question_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(org_home_models.Categories,pk=category_id)
    question = get_object_or_404(Question,pk=question_id)
    percentVoted = str((len(question.voters.all())/len(category.members.all()))*100)
    return render(request,'vote/results.html',{
        'organization':organization,
        'category': category,
        'question':question,
        'choice_set':Question.objects.filter(pub_date__lte=timezone.now()),
        'percent_voted':percentVoted,
        'categories_list':Categories.objects.filter(organization=organization),
    })

# submit a vote
@is_member
@login_required
def vote(request,organization_id,category_id,question_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    question = get_object_or_404(Question, pk=question_id)
    category = get_object_or_404(Categories, pk=category_id)
    percentVoted = str(round(float(len(question.voters.all()))/float(len(category.members.all())) * 100,1))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'vote/detail.html', {
            'organization':organization,
            'category': category,
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if request.user in question.voters.all():
            return render(request, 'vote/results.html', {
            'organization':organization,
            'category': category,
            'question': question,
            'choice_set':Question.objects.filter(pub_date__lte=timezone.now()),
            'percent_voted':percentVoted,
            'error_message': "You have already voted",
        })
        # add 1 to the count of the selected option
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # add the user to a list of peo
        question.voters.add(request.user)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('vote:results', args=(organization.id,category_id,question.id)))

@is_member
@login_required
def newPollView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(org_home_models.Categories,pk=category_id)
    return render(request, 'vote/newPoll.html',{'organization':organization,'category':category,'categories_list':Categories.objects.filter(organization=organization)})

@is_member
@login_required
def submitNewPoll(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    category = get_object_or_404(org_home_models.Categories,pk=category_id)
    # make sure there is one question and at least two choices and that they aren't empty
    if 'question' in request.POST and 'choice_1' in request.POST and 'choice_2' in request.POST and request.POST['question'] != "" and request.POST['choice_1'] != "" and request.POST['choice_2'] != "":
        q = Question.objects.create(category = category, question_text=request.POST['question'], pub_date=timezone.now())
        # for every choice_ in POST, check to see if it isn't empty add this choice to the question created above
        for c in request.POST:
            if 'choice' in c and request.POST[c] != "":
                q.choice_set.create(choice_text = request.POST[c])

        discussion = Post.objects.create(
                discussionType='Voting',
                category=category,
                title=q.question_text,
                content=q.question_text,
                pub_date=timezone.now(),
                original_poster=request.user
            )

        q.post = discussion
        q.save()

        # if everything works send to the index page
        return HttpResponseRedirect(reverse('vote:index', args=(organization.id,category.id,)))
    else:
        # if error take back to newPoll page with error message
        return render(request, 'vote/newPoll.html', {
            'organization':organization,
            'error_message': "Please enter a question and a two choices",
            'category': category,
            'categories_list':Categories.objects.filter(organization=organization)
        })
