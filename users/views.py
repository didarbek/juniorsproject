from django.shortcuts import render,get_object_or_404,redirect,resolve_url
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views import generic
from .models import CustomUser
from django.views.generic import ListView
from juniorsproject.decorators import ajax_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Profile
from posts.models import Post
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from utils import check_image_extension
from notifications.models import Notification
from .forms import ProfileEditForm,UserEditForm
import requests
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your views here.

class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')

class FollowersPageView(LoginRequiredMixin,ListView):
    model = User
    paginate_by = 20
    template_name = 'users/followers.html'
    context_object_name = 'users'

    def get_queryset(self,**kwargs):
        return self.request.user.profile.followers.all()

class FollowingPageView(LoginRequiredMixin,ListView):
    model = User
    paginate_by = 20
    template_name = 'users/following.html'
    context_object_name = 'profiles'

    def get_queryset(self,**kwargs):
        return self.request.user.following.all()

@login_required
@ajax_required
def follow_user(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.user in user.profile.followers.all():
        user.profile.followers.remove(request.user)
    else:
        user.profile.followers.add(request.user)
        Notification.objects.create(
            Actor=request.user,
            Target=user,
            notif_type='follow'
        )
        text = 'Unfollow'
    return HttpResponse(text)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST)
        if user_form.is_valid():
            user_form.save()
        else:
            user_form = UserEditForm(instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
        else:
            profile_form = ProfileEditForm(instance=request.user.profile)
        msg_txt = """
            <p>Your profile info is successfully saved. <a href="/" class="alert-link">Go to homepage</a></p>
        """
        messages.success(request,msg_txt)
        return redirect('profile_edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'users/profile_edit.html',{'user_form':user_form,'profile-form':profile_form})

@login_required
def change_picture(request):
    if request.method == 'POST':
        user_dp = request.FILES.get('dp')
        if check_image_extension(user_dp.name):
            profile_form = Profile.objects.get(user=request.user)
            profile_form.dp = user_dp
            profile_form.save()
            msg_txt = """
                <p>Your profile picture is successfully saved. <a href="/" class="alert-link">Go to homepage</a></p>
            """
            messages.success(request,msg_txt)
        else:
            msg_txt = """
                <p>
                    Filetype not supported. Please use .jpg or .png filetypes.
                    <a href="/" class="alert-link">Go to homepage</a>
                </p>
            """
            messages.warning(request,msg_txt)
            return redirect('picture_change')
        return redirect('user_profile',username=request.user.username)
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,'users/change_picture.html',{'profile_form':profile_form})

class UserProfilePageView(LoginRequiredMixin,ListView):
    model = Post
    paginate_by = 15
    template_name = 'users/profile.html'
    context_object_name = 'posts'

    def get_queryset(self,**kwargs):
        self.user = get_object_or_404(User,username=self.kwargs['username'])
        return Post.get_posts(self.user)

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context["user"] = self.user
        return context
