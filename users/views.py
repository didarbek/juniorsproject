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

