from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.    

class Interests(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, default='')
    country = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    avatar = models.ImageField(null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    facebook_link = models.URLField(max_length=200)
    github_link = models.URLField(max_length=200)
    instagram_link = models.URLField(max_length=200)
    twitter_link = models.URLField(max_length=200)
    interests = models.ForeignKey(Interests,on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User, related_name='following', blank=True
    )
    contact_list = models.ManyToManyField(
        User, related_name='contacters', blank=True
    )
    pending_list = models.ManyToManyField(
        User, related_name='my_pending_requests', blank=True
    )

    def __str__(self):
        return self.user
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
