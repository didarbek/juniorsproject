from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from users.models import CustomUser
from groups.models import Group

def SubscriptionList(self):
    groups = Group.objects.all()
    return {"groups":groups}
