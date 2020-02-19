from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from slugify import UniqueSlugify
from datetime import timedelta
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

# Create your models here.

class Group(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500)
    cover = models.ImageField(upload_to='group_covers/', blank=True, null=True)
    admins = models.ManyToManyField(User, related_name='inspected_groups')
    subscribers = models.ManyToManyField(User, related_name='subscribed_groups')
    banned_users = models.ManyToManyField(User, related_name='forbidden_groups')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
     
    class Meta:
        ordering = ('-created')

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = group_slugify(f"{self.title}")
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('group',args=[self.slug])
    
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
        raise ValidationError("You can't assign more than three admins.")
m2m_changed.connect(admins_changed,sender=Group.admins.through)

def group_unique_check(text,uids):
    if text in uids:
        return False
    return not Group.objects.filter(slug=text).exists()

group_slugify = UniqueSlugify(
                    unique_check=group_unique_check,
                    to_lower=True,
                    max_length=80,
                    separator='_',
                    capitalize=False
                )
                