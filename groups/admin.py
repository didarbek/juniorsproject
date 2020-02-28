from django.contrib import admin
from .models import Group

# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'created'
admin.site.register(Group, GroupAdmin)
