from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from notifications.models import Notification
from posts.models import Post
from users.api.serializers import UserDetailSerializer
from django.conf import settings

User = settings.AUTH_USER_MODEL

class PostSerializer(serializers.ModelSerializer):
    body_linkified = serializers.SerializerMethodField()
    author = UserDetailSerializer(read_only=True)
    group_slug = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True)
    created_naturaltime = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'body', 'body_linkified',
            'photo', 'author', 'group', 'group_slug',
            'comments_count', 'created',
            'created_naturaltime', 'is_author',
        ]
    
    def get_body_linkified(self,obj):
        return obj.linkfy_post()

    def get_group_slug(self,obj):
        return obj.group.slug

    def get_stars_count(self,obj):
        return obj.points.all().count()

    def get_comments_count(self,obj):
        return obj.comments.all().count()

    def get_created_naturaltime(self,obj):
        return naturaltime(obj.created)

    def get_is_author(self,obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user = request.user
        if user == obj.author:
            return True
        return False
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        title = validated_data['title']
        body = validated_data['body']
        words = title + ' ' + body
        words_list = words.split(" ")
        names_list = []
        for word in words_list:
            if word[:2] == "u/":
                username = word[2:]
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user not in names_list:
                        instance.mentioned.add(user)
                        if user is not mentioned_user:
                            Notification.objects.create(
                                Actor=user,
                                Object=instance,
                                Target=mentioned_user,
                                notif_type='post_mentioned'
                            )
                        names_list.append(user)
                except:
                    pass
        return instance