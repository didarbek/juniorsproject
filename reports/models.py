from django.db import models
from django.conf import settings
from groups.models import Group
from comments.models import Comment
from posts.models import Post

# Create your models here.

User = settings.AUTH_USER_MODEL

class Report(models.Model):
    reporter = models.ForeignKey(User,related_name='reported',null=True,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,related_name='comment_reports',blank=True,null=True,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='post_reports',blank=True,null=True,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,related_name='group_reports',blank=True,null=True,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        if self.comment:
            return '{} reported a comment {}.'.format(
                self.reporter.profile.screen_name(),self.comment.body
            )
        else:
            return '{} reported a post entitled \"{}\" posted by \"{}\".'.format(
                self.reporter.profile.screen_name(),
                self.post, self.post.author
            )

    @staticmethod
    def get_reports(groups_slug=None):
        if groups_slug:
            reports = Report.objects.filter(active=True,
                                            group__slug__icontains=groups_slug)
        else:
            reports = Report.objects.filter(active=True)
        return reports
