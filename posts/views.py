from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
import requests
from comments.forms import CommentForm
from notifications.models import Notification
from utils import image_compression
from .decorators import user_is_post_author
from .forms import PostForm
from .models import Post
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your views here.

# def get_trending_posts():
#     try:
#         posts = Post.get_posts()
#         for post in posts:
#             post.set_rank()
#         trending_posts = posts.order_by('-rank_score')
#     except OperationalError:
#         trending_posts = None
#     return trending_posts

def get_home_posts():
    try:
        home_posts = Post.get_posts()
    except OperationalError:
        home_posts = None
    return home_posts

class HomePostView(ListView):
    model = Post
    queryset = get_home_posts()
    paginate_by = 15
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

    


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'detail'
