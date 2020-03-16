from .forms import CustomUserCreationForm
from django.views import generic
from django.urls import  reverse_lazy
from .forms import UserEditForm, UserEditForm, ProfileForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.shortcuts import render, get_object_or_404
import os 
from django.http import  HttpResponseRedirect, HttpResponse
from .models import  CustomUser, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from comments.models import Comment
from itertools import chain
from groups.models import Group
from notifications.models import Notification
from django.core.paginator import  Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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
    user_groups_admin = Group.objects.filter(admins=id).order_by('-created')[:5]
    result_post =  sorted(chain(user_posts,user_comments), key=lambda instance: instance.created, reverse=True)
    print(result_post)
    return render(request, 'show_user_profile.html', {'user_list':user_base, 'user_profile':user_profile,'user_posts':user_posts,'user_comments':user_comments,'user':user,'result_post':result_post,'user_groups_admin':user_groups_admin})

class FollowersPageView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'profile/followers.html'
    context_object_name = 'user_followers'
    
    def get_queryset(self, **kwargs):
        print("this for followers user : {0} ".format(self.request.user.profile.followers.all()))
        return self.request.user.profile.followers.all()



class FollowingPageView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'profile/following.html'
    context_object_name = 'profiles'

    def get_queryset(self, **kwargs):
        # print("this for following user :{0} ".format(self.request.user.following.count))
        # print("this for followers user : {0} ".format(self.request.user.profile.following.count()))
        return self.request.user.following.all()
    

def follow_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user in user.profile.followers.all():
        user.profile.followers.remove(request.user)
        text = 'Follow'
    else:
        user.profile.followers.add(request.user)
        text = 'Unfollow'
    return HttpResponse(text)
    

@login_required
def send_message_request(request, user_id):
    receiver = get_object_or_404(CustomUser, id=user_id)
    contacter = request.user 

    if contacter in receiver.profile.pending_list.all():
        receiver.profile.pending_list.remove(contacter)
        text = 'Send Request'
    else:
        receiver.profile.pending_list.add(contacter)
        Notification.objects.create(Actor=contacter, Target=receiver, notif_type='sent_msg_request')
        text = 'Request Sent'
    return HttpResponse(text)


@login_required
def accept_message_request(request, user_id):
    sender = get_object_or_404(CustomUser, id=user_id)
    acceptor = request.user 

    if sender in acceptor.profile.pending_list.all():
        acceptor.profile.pending_list.remove(sender)
        acceptor.profile.contact_list.add(sender)
        sender.profile.contact_list.add(acceptor)
        Notification.objects.create(Actor=acceptor, Target=sender,  notif_type='confirmed_msg_request')
        text = 'Added to contact list'
    else:
        text = 'Unexpected error!'
    return HttpResponse(text)


@login_required
def all_message_requests(request):
    message_requests = request.user.profile.pending_list.all()
    paginator = Paginator(message_requests, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True 
    else:
        p = False 
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    
    except  EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    p_obj = users 

    return render(request, 'profile/view_all_message_requests.html',{
        'users':users,
        'page':page,
        'p':p,
        'p_obje':p_obj
    })

        
@login_required
def all_friends(request):
    user_contact_list = request.user.profile.contact_list.all() 
    paginator = Paginator(user_contact_list, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        users = paginator.page(page)

    except PageNotAnInteger:
        users = paginator.page(1)

    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    p_obj = users

    return render(request, 'profile/view_all_contacts.html', {
        'users':users,
        'page':page,
        'p':p,
        'p_obj':p_obj
    })
