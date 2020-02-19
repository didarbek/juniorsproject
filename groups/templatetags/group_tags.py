import random
from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import markdown
from ..models import Group

register = template.Library()

@register.inclusion_tag('includes/group_container.html')
def group_container_items(user):
    groups_list = user.subscribed_groups.all()
    return {'groups_list':groups_list,'user':user}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.inclusion_tag('includes/active_threads.html')
def show_active_threads(user):
    current_user = User.objects.get(id=user.id)
    threads = current_user.posted_subjects.all()[:5]
    return {'threads':threads}
    