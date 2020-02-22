from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.

class Notification(models.Model):

    NOTIF_CHOICES = (
        ('post_mentioned', 'Mentioned in Post'),
        ('comment_mentioned', 'Mentioned in Comment'),
        ('comment', 'Comment on Post'),
        ('follow', 'Followed by someone'),
        ('sent_msg_request', 'Sent a Message Request'),
        ('confirmed_msg_request', 'Sent a Message Request'),
    )

    Actor = models.ForeignKey(User, related_name='c_acts', on_delete=models.CASCADE)
    Object = models.ForeignKey(Post, related_name='act_notif', null=True, blank=True, on_delete=models.SET_NULL)
    Target = models.ForeignKey(User, related_name='c_notif', on_delete=models.CASCADE)
    notif_type = models.CharField(
        max_length=500, choices=NOTIF_CHOICES, default='Comment on Post'
    )
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.notif_type == 'comment':
            return '{} commented on your post \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )
        elif self.notif_type == 'post_mentioned':
            return '{} mentioned you in his post \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )
        elif self.notif_type == 'follow':
            return '{} followed you.'.format(
                self.Actor.profile.screen_name()
            )
        elif self.notif_type == 'sent_msg_request':
            return '{} sent you a message request.'.format(
                self.Actor.profile.screen_name()
            )
        elif self.notif_type == 'confirmed_msg_request':
            return '{} accepted your message request.'.format(
                self.Actor.profile.screen_name()
            )
        else:
            return '{} mentioned you in his comment on post \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )

    @staticmethod
    def get_user_notification(user):
        if user:
            notifications = Notification.objects.create(Target=user).exclude(Actor=user)
            return notifications
        return []
        