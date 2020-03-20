from django.core.exceptions import PermissionDenied
from .models import Post

def post_author(f):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['post'])
        if request.user == post.author:
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    