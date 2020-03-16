from django.contrib import admin
from .models import Message

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'conversation', 'message', 'date',)
    list_filter = ('date',)
admin.site.register(Message, MessageAdmin)
