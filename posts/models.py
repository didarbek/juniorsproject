from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
# import bleach
# from slugify import UniqueSlugify
from communities.models import Community

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150,db_index=True)
    slug = models.SlugField(max_length=150,null=True,blank=True)
    body = models.TextField(max_length=5000,null=True,blank=True)
    photo = models.ImageField(upload_to='post_photos/',verbose_name=u"Add image (optional)",blank=True,null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='posted_posts',on_delete=models.CASCADE)
    community = models.ForeignKey(Community,related_name='submitted_posts',on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args={"slug": self.slug})

    @staticmethod
    def get_posts(user=None):
        if user:
            posts = Post.objects.filter(active=True,author=user)
        else:
            posts = Post.objects.filter(active=True)
        return posts

    @staticmethod
    def search_posts(query,community=None):
        if community:
            search_results = Community.object.filter(active=True,title__icontains=query,community=community)
        else:
            search_results = Community.objects.filter(active=True,title__icontains=query)
        return search_results