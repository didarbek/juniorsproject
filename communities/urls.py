from django.urls import re_path
from .views import UserSubscriptionListView, CommunitiesPageView, edit_community_cover, subscribe, new_community, UserCreatedCommunitiesPageView
app_name = 'communities'

urlpatterns = [
    re_path(r'^u/(?P<username>[\w.@+-]+)/subscriptions/$',UserSubscriptionListView.as_view(),name='user_subscription_list'),
    # re_path(r'^trending/$',posts_views.TrendingPageView.as_view(), name='trending'),
    # re_path(r'^b/$',CommunitiesPageView.as_view(), name='view_all_communities'),
    # re_path(r'^b/(?P<community>[-\w]+)/$',communities_views.CommunityPageView.as_view(),name='community'),
    # re_path(r'^b/ban_user/(?P<community>[-\w]+)/(?P<user_id>\d+)/$',ban_user,name='ban_user'),
    # re_path(r'^b/(?P<community>[-\w]+)/edit_community_cover/$',edit_community_cover,name='edit_community_cover'),
    # re_path(r'^b/(?P<community>[-\w]+)/subscription/$',subscribe,name='subscribe'),
    # re_path(r'^b/(?P<post>[-\w]+)/like/$',like_post,name='like'),
    # re_path(r'^load_new_comments/$',load_new_comments, name='load_new_comments'),
    # re_path(r'^u/(?P<username>[\w.@+-]+)/communities/$',UserCreatedCommunitiesPageView.as_view(),name='user_created_communities'),
    # re_path(r'^u/(?P<username>[\w.@+-]+)/communities/$',UserCreatedCommunitiesPageView.as_view(),name='user_created_communities'),

    # re_path(r'^delete_comment/(?P<pk>\d+)/$',delete_comment, name='delete_comment'),
    # re_path(r'^new_community/$',new_community, name='new_community'),

]
