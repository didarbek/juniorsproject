from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('groups/',views.GroupsPage.as_view(),name='view_all_groups'),
    path('groups/<group>/',views.GroupPage.as_view(),name='group'),
    path('groups/ban_user/<group>/<user_id>/',views.ban_user,name='ban_user'),
    path('groups/<group>/edit_group_cover/',views.edit_group_cover,name='edit_group_cover'),
    path('groups/<group>/subscription/',views.subscribe,name='subscribe'),
    path('<username>/groups/',views.UserCreatedGroupsPage.as_view(),name='user_created_groups'),
    path('create_group/',views.create_group, name='create_group'),
    path('groups/<username>/subscriptions/',views.UserSubscriptionList.as_view(),name='user_subscription_list'),
    path('group/result/', views.GroupSearch.as_view(), name='group_search')
]
