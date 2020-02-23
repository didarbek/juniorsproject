from django.contrib import admin
from .models import Report

# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'created', 'active')
    list_filter = ('active',)
    date_hierarchy = 'created'
admin.site.register(Report, ReportAdmin)