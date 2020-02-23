from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from communities.models import Community
from comments.models import Comment
from juniorsproject.decorators import ajax_required
from posts.models import Post
from .models import Report

# Create your views here.

@login_required
@ajax_required
def report_post(request,post):
    post = get_object_or_404(Post,slug=post)
    community = post.community
    rep = request.user
    Report.objects.create(reporter=rep,
                         post=post,
                         community=community)
    return HttpResponse('Report has been sent to admins.')

@login_required
@ajax_required
def report_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    rep = request.user
    community = comment.post.community
    Report.objects.create(reporter=rep,
                          comment=comment,
                          community=community)
    return redirect('post_detail',community=community.slug,post=comment.post.slug)

@login_required
def show_reports(request,community):
    community = get_object_or_404(Community,slug=community)
    admins = community.admins.all()
    if request.user in admins:
        reports = community.community_reports.filter(active=True)
        bv = True
        return render(request,'reports/show_reports.html',{
            'reports':reports,
            'community':community,
            'bv':bv,
            'admins':admins
        })