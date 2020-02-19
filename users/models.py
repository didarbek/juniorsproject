from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser): 
    email =  models.EmailField(_('email address'), unique=True)
    username =  models.EmailField(_('username'), unique=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email

