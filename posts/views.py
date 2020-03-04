from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DeleteView,RedirectView
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
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions
from .serializers import CommentSerializer
from comments.models import Comment
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime
from juniorsproject.decorators import ajax_required

# # Create your views here.

User = settings.AUTH_USER_MODEL

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
    context = {}
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commenter = request.user
            new_comment.post = post
            new_comment.save()
            new_comment_id = new_comment.id
            body = request.POST.get('body')
            context['body'] = body
            context['id'] = new_comment_id
            context['date'] = str(naturaltime(new_comment.created))
            context['username'] = str(request.user.username)
            context['delete'] = str(reverse('comments:delete_comment',args=[new_comment.id]))
            return JsonResponse(context)
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

# class PostLikeToggle(RedirectView):
#     def get_redirect_url(self,*args,**kwargs):
#         slug = self.kwargs.get("slug")
#         post = get_object_or_404(Post,slug=slug)
#         url_ = post.get_absolute_url()
#         user = self.request.user
#         if user.is_authenticated:
#             if user in post.points.all():
#                 post.points.remove(user)
#             else:
#                 post.points.add(user)
#         return url_

# class PostLikeAPIToggle(APIView):
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#     def get(self,request,slug=None,format=None):
#         post = get_object_or_404(Post,slug=slug)
#         url_ = post.get_absolute_url()
#         user = self.request.user
#         updated = False
#         liked = False
#         if user.is_authenticated:
#             if user in post.points.all():
#                 liked = False
#                 post.points.remove(user)
#             else:
#                 liked = True
#                 post.points.add(user)
#             updated = True
#         data = {
#             "updated":updated,
#             "liked":liked
#         }
#         return Response(data)

@login_required
@ajax_required
def like_subject(request,post):
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

class SearchView(ListView):
    model = Post
    template_name = 'posts/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('title','body')
        object_list = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return object_list
