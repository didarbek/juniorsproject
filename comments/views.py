from django.shortcuts import render,get_object_or_404,redirect, Http404
from django.contrib.auth.decorators import login_required
from .decorators import user_is_comment_owner
from .models import Comment
from posts.models import Post
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from posts.models import Post
from django.http import JsonResponse
# Create your views here.

def _html_comments(comment_id,group,post):
    post = get_object_or_404(Post,group__slug=group.slug,slug=post.slug)
    comment = post.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(html,render_to_string('comments/post_comments.html',{'comment':comment,'user':user}))
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


# class DeleteComment(generic.DeleteView):
#     model = Comment
#     success_url = 'posts:'

@login_required
@user_is_comment_owner

def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)

    comment.delete()
    return ''   