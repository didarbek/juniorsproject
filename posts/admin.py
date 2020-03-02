from django.contrib import admin
from .models import Post
from comments.models import Comment
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    verbose_name_plural = 'Comment'
    fk_name = 'post'

class CustomPostAdmin(admin.ModelAdmin):
    inlines = (CommentInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list() 
        return super(CustomPostAdmin, self).get_inline_instances(request, obj)



admin.site.register(Post, CustomPostAdmin)