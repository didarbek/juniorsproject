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
    re_path(r'^trending/$',posts_views.TrendingPageView.as_view(), name='trending'),
    re_path(r'^s/(?P<community>[-\w]+)/(?P<post>[-\w]+)/$',
        posts_views.post_detail,
        name='post_detail'),
    re_path(r'^b/$',communities_views.CommunitiesPageView.as_view(), name='view_all_communities'),
    re_path(r'^b/(?P<community>[-\w]+)/$',
        communities_views.CommunityPageView.as_view(),
        name='community'),
    re_path(r'^b/ban_user/(?P<community>[-\w]+)/(?P<user_id>\d+)/$',
        communities_views.ban_user,
        name='ban_user'),
    re_path(r'^b/(?P<community>[-\w]+)/edit_community_cover/$',
        communities_views.edit_community_cover,
        name='edit_community_cover'),
    re_path(r'^b/(?P<community>[-\w]+)/subscription/$',
        communities_views.subscribe,
        name='subscribe'),
    re_path(r'^b/(?P<post>[-\w]+)/like/$',
        posts_views.like_post,
        name='like'),
    re_path(r'^load_new_comments/$', comments_views.load_new_comments, name='load_new_comments'),
    re_path(r'^u/(?P<username>[\w.@+-]+)/subscriptions/$',communities_views.UserSubscriptionListView.as_view(),
        name='user_subscription_list'),
    re_path(r'^u/(?P<username>[\w.@+-]+)/communities/$',communities_views.UserCreatedCommunitiesPageView.as_view(),
        name='user_created_communities'),
    re_path(r'^u/(?P<username>[\w.@+-]+)/communities/$',communities_views.UserCreatedCommunitiesPageView.as_view(),
        name='user_created_communities'),
    re_path(r'^new_post/$',posts_views.new_post, name='new_post'),
    re_path(r'^delete_post/(?P<post>[-\w]+)/$',posts_views.delete_post, name='delete_post'),
    re_path(r'^edit_post/(?P<post>[-\w]+)/$', posts_views.edit_post, name='edit_post'),
    re_path(r'^delete_comment/(?P<pk>\d+)/$', comments_views.delete_comment, name='delete_comment'),
    re_path(r'^new_community/$',communities_views.new_community, name='new_community'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
