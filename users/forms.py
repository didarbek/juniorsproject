from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from django.conf import settings
from .models import Profile
from django.forms.widgets import ClearableFileInput
from bootstrap_datepicker_plus import DatePickerInput

User = settings.AUTH_USER_MODEL


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'profile/custom_clear_file_input.html'


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None 

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','email')


class ProfileForm(forms.ModelForm):
    # img_profile = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ('img_profile', 'birth_date', 'gender', 'country')
        widgets = {
            'img_profile':CustomClearableFileInput(),
            'birth_date':DatePickerInput(format='%m/%d/%Y')
        }
    
 

