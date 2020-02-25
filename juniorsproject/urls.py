"""juniorsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home,groups,group_detail, post
import communities.views as communities_views
import comments.views as comments_views
import notifications.views as notifications_views
import reports.views as reports_views
import search.views as search_views
import posts.views as posts_views
import users.views as users_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('groups/',groups,name='groups'),
    path('group_detail/',group_detail,name='group_detail'),
    path('post/', post, name='post'),
    path('account/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('communities.urls')),
    path('', include('comments.urls')),
    path('', include('posts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
