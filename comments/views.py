from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
# from mysite.decorators import ajax_required
from posts.models import Post
from .decorators import user_is_comment_owner
from .models import Comment

# Create your views here.

def _html_comments(comment_id,community,post):
    post = get_object_or_404(Post,community__slug=community.slug,slug=post.slug)
    comment = post.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(html,render_to_string('comments/partial_post_comments.html',{'comment':comment,'user':user}))
    return html

@ajax_required
def load_new_comments(request):
    last_comment_id = request.GET.get('last_comment_id')
    community = request.GET.get('community')
    post = request.GET.get('post')
    user = request.user
    post = get_object_or_404(Post,community__slug=community,slug=post)
    comments = post.comments.filter(id__gt=last_comment_id)
    if comments:
        html = ''
        html = '{0}{1}'.format(html,render_to_string('comments/partial_load_more_comments.html',{'comments':comments,'user':user}))
        return HttpResponse(html)
    else:
        return HttpResponse('')

@login_required
def deactivate_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    admins = comment.post.community.admins.all()
    if request.user in admins:
        reports = comment.comment_reports.all()
        community_reports = comment.post.community.community_reports.all()
        for report in reports:
            if report in community_reports:
                comment.active = False
                comment.save()
            else:
                return redirect()
    else:
        return redirect('home')
    return redirect('home')

@login_required
@ajax_required
@user_is_comment_owner
def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return HttpResponse('This comment has been deleted.')
    