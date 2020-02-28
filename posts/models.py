from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from groups.models import Group

# Create your models here.

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    image = models.ImageField(upload_to='post_photos/',blank=True, null=True)
    author = models.ForeignKey(User, related_name='posted_posts', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='submitted_posts', on_delete=models.CASCADE)
    points = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    mentioned = models.ManyToManyField(User, related_name='m_in_posts', blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.group.slug,
                             self.slug])

    @staticmethod
    def get_posts(user=None):
        if user:
            posts = Post.objects.filter(active=True,author=user)
        else:
            posts = Post.objects.filter(active=True)
        return posts
        