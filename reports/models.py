from django.db import models
from comments.models import Comment
from posts.models import Post
from communities.models import Community

from django.conf import  settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Report(models.Model):
    reporter = models.ForeignKey(User, related_name='reported', null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(
        Comment, related_name='comment_reports', blank=True, null=True, on_delete=models.SET_NULL
    )
    post = models.ForeignKey(
        Post,related_name='post_reports', blank=True, null=True, on_delete=models.SET_NULL
    )
    community = models.ForeignKey(
        Community, related_name='community_reports', blank=True, null=True, on_delete=models.SET_NULL
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.comment:
            return '{} reported a comment.'.format(
                self.reporter.profile.screen_name()
            )
        else:
            return '{} reported a subject entitled \"{}\" posted by \"{}\".'.format(
                self.reporter.profile.screen_name(),
                self.post, self.post.author
            )
    
    @staticmethod
    def get_reports(communities_slug=None):
        """Returns a list of reports."""
        if communities_slug:
            reports = Report.objects.filter(active=True,
                                            communities__slug__icontains=communities_slug)
        else:
            reports = Report.objects.filter(active=True)
        return reports
        