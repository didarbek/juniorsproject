from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Post
from .decorators import post_author
from django.db import OperationalError
from .forms import PostForm
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from comments.forms import CommentForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from django.core import serializers
from users.models import Profile
# # Create your views here.
User = settings.AUTH_USER_MODEL

def home(request):
    return render(request,'posts/posts.html')

def get_home_posts():
    try:
        home_posts = Post.get_posts()
    except OperationalError:
        home_posts = None
    return home_posts

class HomePage(ListView):
    model = Post
    queryset = get_home_posts()
    paginate_by = 15
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
def _html_comments(comment_id,group,post):
    post = get_object_or_404(Post,group__slug=group.slug,slug=post.slug)
    comment = post.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(html,render_to_string('comments/comments.html',{'comment': comment,'user': user,}))
    return html



def post_detail(request,group,post):
    post = get_object_or_404(Post,group__slug=group,slug=post)
    comments = post.comments.filter(active=True)
    group = post.group
    user = request.user
    admins = group.admins.all()
    new_comment = None
    response_data = {}
    if request.user.is_authenticated:
        if request.method == 'POST' and request.is_ajax :
            comment_form = CommentForm(data=request.POST or None)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.commenter = request.user
                new_comment.post = post
                new_comment.save()
                new_comment_id = new_comment.id
                serial_user = serializers.serialize('json',[new_comment])
                serial_username  = serializers.serialize('json',[comments])
                response_data['user'] = serial_user
                response_data['username'] = serial_username
                return JsonResponse(response_data)
                # return HttpResponseRedirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'new_comment':new_comment,
        'comment_form':comment_form,
        'post':post,
        'comments':comments,
        'group':group,
        'admins':admins,
    })


@login_required
def new_post(request):
    post_form = PostForm(**{'user':request.user})
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            author = request.user
            new_post.author = author
            new_post.save()
            new_post.points.add(author)
            new_post.save()
            return redirect(new_post.get_absolute_url())
    else:
        post_form = PostForm()
    return render(request,'posts/create_post.html',{'post_form':post_form})

@login_required
def like_post(request,post):
    data = dict()
    post = get_home_posts(Post,slug=post)
    user = request.user
    if post in user.liked_posts.all():
        post.points.remove(user)
        data['is_starred'] = False
    else:
        post.points.add(user)
        data['is_starred'] = True
    data['total_points'] = post.points.count()
    return reverse('posts:post',args=[self.slug])

@login_required
@post_author
def delete_post(request,post):
    post = get_object_or_404(Post,slug=post)
    post.delete()
    return HttpResponseRedirect(reverse('posts:home'))

@login_required
@post_author
def edit_post(request,post):
    post = get_object_or_404(Post,slug=post)
    if request.method == 'POST':
        post_form = PostForm(instance=post,data=request.POST,files=request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect(post.get_absolute_url())
        else:
            post_form = PostForm(instance=post)
    else:
        post_form = PostForm(instance=post)
    return render(request,'posts/edit_post.html',{'post_form':post_form})
