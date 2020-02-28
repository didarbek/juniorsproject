from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Post
from .decorators import post_author
from django.db import OperationalError
from .forms import PostForm
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

# # Create your views here.

User = settings.AUTH_USER_MODEL

def home(request):
    return render(request,'posts/posts.html')

def post_detail(request):
    return render(request,'posts/post_detail.html')
    
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
                            u = word[2:]
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
                    html = _html_comments(new_comment_id,group,post)
                    return HttpResponse(html)

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
    return JsonResponse(data)

@login_required
@post_author
def delete_post(request,post):
    post = get_object_or_404(Post,slug=post)
    post.delete()
    return HttpResponse('Post has been deleted.')

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
