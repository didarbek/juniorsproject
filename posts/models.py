from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from groups.models import Group
from slugify import UniqueSlugify
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
    rank_score = models.FloatField(default=0.0)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = post_slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post_detail',
                       args=[self.group.slug,
                             self.slug])

    def get_like_url(self):
        return reverse("posts:like-toggle",kwargs={"slug":self.slug})
    
    def get_api_like_url(self):
        return reverse("posts:like-api-toggle",kwargs={"slug":self.slug})

    @staticmethod
    def get_posts(user=None):
        if user:
            posts = Post.objects.filter(active=True,author=user)
        else:
            posts = Post.objects.filter(active=True)
        return posts
        
    def set_rank(self):
        GRAVITY = 1.2
        time_delta = timezone.now() - self.created
        post_hour_age = time_delta.total_seconds()
        post_points = self.points.count() - 1
        self.rank_score = post_points / pow((post_hour_age + 2), GRAVITY)
        self.save()

def post_unique_check(text, uids):
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
