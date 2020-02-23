from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
import requests
from comments.forms import CommentForm
from juniorsproject.decorators import ajax_required
from notifications.models import Notification
from utils import image_compression
from .decorators import user_is_post_author
from .forms import PostForm
from .models import Post
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your views here.

def get_trending_posts():
    try:
        posts = Post.get_posts()
        for post in posts:
            post.set_rank()
        trending_posts = posts.order_by('-rank_score')
    except OperationalError:
        trending_posts = None
    return trending_posts

def get_home_posts():
    try:
        home_posts = Post.get_posts()
    except OperationalError:
        home_posts = None
    return home_posts

class HomePageView(ListView):
    model = Post
    queryset = get_home_posts()
    paginate_by = 15
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_quote'] = True
        return context

class TrendingPageView(ListView):
    model = Post
    queryset = get_trending_posts()
    paginate_by = 15
    template_name = 'posts/trending.html'
    context_object_name = 'posts'

def _html_comments(comment_id,community,post):
    post = get_object_or_404(Post,community__slug=community.slug,slug=post.slug)
    comment = post.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(html,render_to_string('comments/partial_post_comments.html',{'comment':comment,'user':user}))
    return html

def post_detail(request,community,post):
    post = get_object_or_404(Post,community__slug=community,slug=post)
    comments = post.comments.filter(active=True)
    community = post.community
    bv = True
    user = request.user
    admins = community.admins.all()

    if request.is_ajax():
        if request.user.is_authenticated:
            if request.method == 'POST':
                comment_form = CommentForm(data=request.POST or None)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.commenter = request.user
                    new_comment.post = post
                    new_comment.save()

                    if request.user is not post.author:
                        Notification.objects.create(
                            Actor=new_comment.commenter,
                            Object=new_comment.post,
                            Target=post.author,
                            notif_type='comment'
                        )
                    words = new_comment.body
                    words = words.split(" ")
                    names_list = []
                    for word in words:
                        if word[:2] == "u/":
                            u = word[:2]
                            try:
                                user = User.objects.get(username=u)
                                if user not in names_list:
                                    if request.user is not user:
                                        Notification.objects.create(
                                            Actor=new_comment.commenter,
                                            Object=new_comment.post,
                                            Target=user,
                                            notif_type='comment_mentioned'
                                        )
                                    names_list.append(user)
                            except:
                                pass 
                    new_comment_id = new_comment.id
                    html = _html_comments(new_comment,community,post)
                    return HttpResponse(html)

    return render(request,'posts/post.html',{
        'post':post,
        'comments':comments,
        'community':community,
        'bv':bv,
        'admins':admins
    })

@login_required
def deactivate_post(request,post):
    post = get_object_or_404(Post,slug=post)
    admins = post.community.admins.all()
    if request.user in admins:
        reports = post.post_reports.all()
        community_reports = post.community.community_reports.all()
        for report in reports:
            if report in community_reports:
                post.activate = False
                post.save()
            else:
                return redirect('home')
    else:
        return redirect('home')
    return redirect('home')

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
            words = new_post.title + ' ' + new_post.body
            words = words.split(" ")
            names_list = []
            for word in words:
                if word[:2] == "u/":
                    u = word[2:]
                    try:
                        user = User.objects.get(username=u)
                        if user not in names_list:
                            new_post.mentioned.add(user)
                            if request.user is not user:
                                Notification.objects.create(
                                    Actor=new_post.author,
                                    Object=new_post,
                                    Target=user,
                                    notif_type='post_mentioned'
                                )
                            names_list.append(user)
                    except:
                        pass
            if new_post.photo:
                image_compression(new_post.photo.name)
            return redirect(new_post.get_absolute_url())
    form_filling = True
    return render(request,'posts/new_post.html',{
        'post_form':post_form,'form_filling':form_filling
    })

@login_required
@ajax_required
def like_post(request,post):
    data = dict()
    post = get_object_or_404(Post,slug=post)
    user = request.user
    if post in user.liked_posts.all():
        post.points.remove(user)
        data['is_starred'] = False
    else:
        post.points.add(user)
        data['is_starred'] = True
    data['total_points'] = post.points.count()
    return JsonResponse(data)
    
@login_required
@ajax_required
@user_is_post_author
def delete_post(request,post):
    post = get_object_or_404(Post,slug=post)
    post.delete()
    return HttpResponse('Post has been deleted.')

@login_required
@user_is_post_author
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
    form_filling = True
    return render(request,'posts/edit_post.html',{
        'post_form':post_form,'form_filling':form_filling
    })
    