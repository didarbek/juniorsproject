from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from groups.models import Group
from comments.models import Comment
from posts.models import Post
from juniorsproject.decorators import ajax_required
from .models import Report
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required
@ajax_required
def report_post(request,post):
    post = get_object_or_404(Post,slug=post)
    group = post.group
    rep = request.user
    Report.objects.create(reporter=rep,
                          post=post,
                          group=group)
    return HttpResponse('Report has been sent to admins')

@login_required
@ajax_required
def report_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    rep = request.user
    group = comment.post.group
    Report.objects.create(reporter=rep,
                          comment=comment,
                          group=group)
    return redirect('posts:post_detail',group=group.slug,post=comment.post.slug)


@login_required
@ajax_required
def delete_comment_report(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    report_comment =  get_object_or_404(Report, comment=comment)
    comment.delete()
    report_comment.delete()
    return HttpResponse("Hello world")


@login_required
def show_reports(request,group):
    group = get_object_or_404(Group,slug=group)
    admins = group.admins.all()
    if request.user in admins:
        reports = group.group_reports.filter(active=True)
        bv = True
        page = request.GET.get('page', 1)
        paginator = Paginator(reports,10)
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        return render(request,'reports/show_reports.html',{
            'reports':reports,
            'group':group,
            'bv':bv,
            'admins':admins
        })
        