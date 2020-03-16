from ..models import Group
from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('groups/top_five.html')
def top_five_groups():
    groupslist = Group.objects.all()
    groupslist = sorted(groupslist, key=lambda instance: instance.recent_posts(), reverse=True)[:5]
    return {'groups_list': groupslist, 'top_groups': True}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
