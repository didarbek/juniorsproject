from rest_framework import serializers
from .models import Post
from comments.models import Comment
from rest_framework.renderers import JSONRenderer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
      'body',
        )



