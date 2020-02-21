from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser): 
    email =  models.EmailField(_('email_address'), unique=True, name='email')
    username =  models.CharField(_('username'), unique=True, max_length=128)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def __str__(self):
        return self.email

