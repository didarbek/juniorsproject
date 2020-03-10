
from .forms import CustomUserCreationForm
from django.views import generic
from django.urls import  reverse_lazy
from .forms import UserEditForm, UserEditForm, ProfileForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.shortcuts import render
import os 
from django.http import  HttpResponseRedirect
from .models import  CustomUser, Profile
from posts.models import Post
from comments.models import Comment

# Create your views here.

User = settings.AUTH_USER_MODEL

class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')
    
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'your profile was successfully updated')
        else:
            messages.error(request, 'Please correct that errors in your profile form')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/profile.html', {
        'user_form':user_form,
        'profile_form':profile_form
    })

def user_show_profile(request, id):
    user_base = CustomUser.objects.filter(id=id)
    user_profile = Profile.objects.filter(user_id=id)
    user = request.user
    user_posts = Post.objects.filter(author=id).order_by('-created')
    user_comments = Comment.objects.filter(commenter=id).order_by('-created')

    return render(request, 'show_user_profile.html', {'user_list':user_base, 'user_profile':user_profile,'user_posts':user_posts,'user_comments':user_comments,'user':user})


@login_required
def my_friends(request):
    if request.method == 'POST':
        form = FriendShipForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=1)
            print(user)
            friend_manage = FriendShip(user=request.user, friend=user)
            friend_manage.save()
            return HttpResponseRedirect('/myfriend/')
    else:
        form = FriendShipForm()
    user = request.user
    profile = Profile.objects.get(user=user)
    friends = FriendShip.objects.filter(user=request.user)
    return render(request,'friend.html', {'form':form, 'user':user, 'profile':profile})


def my_view(request):
    # List of this user's friends
    other_user = User.objects.get(pk=2)
    request_user = Friend.objects.add_friend(
        request.user,                               # The sender
        other_user,                                 # The recipient
        message='Hi! I would like to add you')       
    return render(request, 'show_user.html', {'request_user':request_user})
