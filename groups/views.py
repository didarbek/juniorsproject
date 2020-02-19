from django.shortcuts import render
from django.views.generic import ListView
from .models import Group


# Create your views here.

class GroupsPageView(ListView):
    model = Group
    queryset = Group.objects.all()
    paginate_by = 20
    template_name = 'groups/view_all_groups.html'
    context_object_name = 'groups'

    