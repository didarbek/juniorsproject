from django.core.exceptions import PermissionDenied
from .models import Community

def user_is_community_admin(f):
    def wrap(request,*args,**kwargs):
        community = Community.objects.get(slug=kwargs['community'])
        if request.user in community.admins.all():
            return f(request,*args,**kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

def user_is_not_banned_from_community(f):
    def wrap(request,*args,**kwargs):
        community = Community.objects.get(slug=kwargs['community'])
        if not request.user in community.bannned_users.all():
            return f(request,*args,**kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    