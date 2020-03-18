from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
import random
import os
from django.conf import settings
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser): 
    email =  models.EmailField(_('email_address'), unique=True, name='email')
    username =  models.CharField(_('username'), unique=True, max_length=128)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
]

def user_directory_path(instance, filename):
    all_path = 'user_{0}/{1}'.format(instance.user.id, filename)

    return all_path

class Profile(models.Model):
    user = models.OneToOneField(User,  related_name='profile',  on_delete=models.CASCADE)
    img_profile  = models.ImageField(verbose_name='image profile', upload_to=user_directory_path, null=True, blank=True)
    member_since = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(verbose_name='Birth date', blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    country = CountryField()
    followers = models.ManyToManyField(User, related_name='following')
    pending_list = models.ManyToManyField(User, related_name='my_pending_list')
    contact_list = models.ManyToManyField(User, related_name='contacters', blank=True)

    def __str__(self):
        return self.user.username
    
    def screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:  
            return self.user.username

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/default_picture.png'
        if self.img_profile:
            return self.img_profile.url
        else:
            return default_picture

    def get_number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def save(self, *args, **kwargs):
    slug = slugify(self.username)
    self.slug = slug
    print(slug)
    super().save(*args, **kwargs)
    