import random
from django import template
from django.utils.safestring import mark_safe
import markdown
from django.conf import settings
from ..models import Community
register = template.Library()

User = settings.AUTH_USER_MODEL

@register.inclusion_tag('includes/communities_container.html')
def communities_container_items(user):
    community_list = user.subscribed_communities.all()
    return {'community_list':community_list,'user':user}

@register.inclusion_tag('includes/top_five.html')
def top_five_communities():
    communitylist = Community.objects.all()
    communitylist = sorted(communitylist,key=lambda instance:instance.recent_posts(),reverse=True)[:5]
    return {'community_list':communitylist,'top_communities':True}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.inclusion_tag('includes/active_threads.html')
def show_active_threads(user):
    current_user = User.objects.get(id=user.id)
    threads = current_user.posted_subjects.all()[:5]
    return {'threads':threads}
    