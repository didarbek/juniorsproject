from django.shortcuts import render,redirect
from .models import Profile
from .forms import UserRegistrationForm,ProfileRegistrationForm
from django.contrib import messages


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        p_reg_form = ProfileRegistrationForm(request.POST)
        if form.is_valid() and p_reg_form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            p_reg_form = ProfileRegistrationForm(request.POST, instance=user.profile)
            p_reg_form.full_clean()
            p_reg_form.save()
            messages.success(request, f'Your account has been sent for approval!')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
        p_reg_form = ProfileRegistrationForm()
    return render(request, 'registration/signup.html',{
        'form': form,
        'p_reg_form': p_reg_form
        })
