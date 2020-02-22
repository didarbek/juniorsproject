from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name='posted_comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    reply = models.ForeignKey(
        "Comment", related_name='comment_reply', null=True, blank=True, on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    @staticmethod
    def get_comments(post_slug=None):
        if post_slug:
            comments = Comment.objects.filter(active=True,post__slug__icontains=post_slug)    
        else:
            comments = Comment.objects.filter(active=True)
        return comments
