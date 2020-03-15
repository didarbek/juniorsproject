from django.db import models
from django.conf import settings
from django.db.models import Max

# Create your models here.

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)
        db_table = 'messages_message'

    def __str__(self):
        return self.message
    
    @staticmethod
    def send_message(from_user,to_user,message):
        message = message[:1000]
        current_user_message = Message(from_user=from_user,
                                       message=message,
                                       user=from_user,
                                       conversation=to_user,
                                       is_read=True)
        current_user_message.save()
        Message(from_user=from_user,
                message=message,
                user=to_user,
                conversation=from_user).save()
        return current_user_message

    @staticmethod
    def get_conversations(user):
        conversations = Message.objects.filter(user=user).values('conversations').annotate(last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user':User.objects.get(pk=conversation['conversation']),
                'last':conversation['last'],
                'unread':Message.objects.filter(user=user,
                                                conversation_pk=conversation[
                                                    'conversation'],
                                                    is_read=False).count()
            })
        return users
