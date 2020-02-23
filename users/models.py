from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class CustomUser(AbstractUser): 
    email =  models.EmailField(_('email_address'), unique=True, name='email')
    username =  models.CharField(_('username'), unique=True, max_length=128)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='profile',on_delete=models.CASCADE)
    dp = models.ImageField(upload_to='dps/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    followers = models.ManyToManyField(
        User, related_name='following', blank=True
    )
    contact_list = models.ManyToManyField(
        User, related_name='contacters', blank=True
    )
    pending_list = models.ManyToManyField(
        User, related_name='my_pending_requests', blank=True
    )
    member_since = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-member_since', )
    
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
        default_picture = settings.STATIC_URL + 'img/ditto.jpg'
        if self.dp:
            return self.dp.url
        else:
            return default_picture

@receiver(post_save,sender=User)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

    



    