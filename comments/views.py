from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .decorators import user_is_comment_owner
from .models import Comment
from posts.models import Post
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.

def _html_comments(comment_id,group,post):
    post = get_object_or_404(Post,group__slug=group.slug,slug=post.slug)
    comment = post.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(html,render_to_string('commets/post_comments.html',{'comment':comment,'user':user}))
    return html

@login_required
def deactivate_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    admins = comment.post.group.admins.all()
    if request.user in admins:
        reports = comment.comment_reports.all()
        group_reports = comment.post.group.group_reports.all()
        for report in reports:
            if report in group_reports:
                comment.active = False
                comment.save()
            else:
                return redirect('posts:home')
    else:
        return redirect('posts:home')
    return redirect('posts:home')

@login_required
@user_is_comment_owner
def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return HttpResponse('This comment has been deleted.')
