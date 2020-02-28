from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

User = settings.AUTH_USER_MODEL

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img_profile  = models.ImageField(verbose_name='Your image', upload_to='ProfileImage/%Y/%m/%d/')
    birth_date = models.DateField(verbose_name='Birth date', blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    countries = CountryField()

    def screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    