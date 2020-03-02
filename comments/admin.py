from django.contrib import admin
from .models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','body', 'commenter', 'created', 'active')
    list_filter = ('commenter', 'active')
    date_hierarchy = 'created'
admin.site.register(Comment, CommentAdmin)