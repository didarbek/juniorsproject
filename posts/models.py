from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
import bleach
from slugify import UniqueSlugify
from communities.models import Community

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150,db_index=True)
    slug = models.SlugField(max_length=150,null=True,blank=True)
    body = models.TextField(max_length=5000,null=True,blank=True)
    photo = models.ImageField(upload_to='post_photos/',verbose_name=u"Add image (optional)",blank=True,null=True)
    author = models.ForeignKey(User,related_name='posted_posts',on_delete=models.CASCADE)
    community = models.ForeignKey(Community,related_name='submitted_posts',on_delete=models.CASCADE)
    points = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked_posts',blank=True)
    mentioned = models.ManyToManyField(User,related_name='m_in_posts',blank=True)
    rank_score = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = post_slugify(f"{self.title}")
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('post_detail',
        args=[self.board.slug,
        self.slug])

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

    def get_points(self):
        return self.points.count()

    def linkfy_subject(self):
        return bleach.linkify(escape(self.body))

    def set_rank(self):
        GRAVITY = 1.2
        time_delta = timezone.now - self.created
        post_hour_age = time_delta.total_seconds()
        post_points = self.points.count() - 1
        self.rank_score = post_points / pow((post_hour_age + 2),GRAVITY)
        self.save()

def post_unique_check(text,uids):
    if text in uids:
        return False
    return not Post.objects.filter(slug=text).exists()

post_slugify = UniqueSlugify(
    unique_check=post_unique_check,
    to_lower=True,
    max_length=80,
    separator='_',
    capitalize=False
)
