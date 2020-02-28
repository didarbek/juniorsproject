from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Notification

# Create your views here.

class ActivitiesPage(LoginRequiredMixin,ListView):
    model = Notification
    paginate_by = 20
    template_name = 'notifications/activities.html'
    context_object_name = 'events'

    def get_queryset(self,**kwargs):
        post_events = Notification.objects.filter(Target=self.request.user).exclude(Actor=self.request.user)
        unread_post_events = post_events.filter(is_read=False)
        for notification in unread_post_events:
            notification.is_read = True
            notification.save()
        return post_events

@login_required
def check_activities(request):
    post_events = Notification.objects.filter(Target=request.user,is_read=False).exclude(Actor=request.user)
    return HttpResponse(len(post_events))
    