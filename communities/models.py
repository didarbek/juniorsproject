from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.db.models.signals import m2m_changed
from django.utils import timezone
from slugify import UniqueSlugify

# Create your models here.

class Community(models.Model):
    title = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,null=True,blank=True)
    description = models.TextField(max_length=500)
    cover = models.ImageField(upload_to='community_covers/',blank=True,null=True)
    admins = models.ManyToManyField(User,related_name='inspected_communities')
    subscribers = models.ManyToManyField(User,related_name='subscribed_communities')
    bannned_users = models.ManyToManyField(User,related_name='forbidden_communities')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = community_slugify(f"{self.title}")
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('community',args=[self.slug])
    
    def get_admins(self):
        return self.admins.all()

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/cover.png'
        if self.cover:
            return self.cover.url
        else:
            return default_picture
        
    def recent_posts(self):
        return self.submitted_subjects.filter(created__gte=timezone.now() - timedelta(days=3)).count()

def admins_changed(sender,**kwargs):
    if kwargs['instance'].admins.count() > 3:
        raise ValidationError("You can't assign more than three admins")
m2m_changed.connect(admins_changed,sender=Community.admins.through)

def community_unique_check(text,uids):
    if text in uids:
        return False
    return not Community.objects.filter(slug=text).exists()

community_slugify = UniqueSlugify(
    unique_check=community_unique_check,
    to_lower=True,
    max_length=80,
    separator='_',
    capitalize=False
)
