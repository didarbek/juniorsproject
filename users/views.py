from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views import generic
from .models import CustomUser
# Create your views here.

class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')


