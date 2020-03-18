from django.urls import path
from .views import (ActiveThreadsList, StarPostView, PosttListCreateAPIView,PostRetrieveUpdateDestroyAPIView,)

urlpatterns = [
    path('posts/',PostListCreateAPIView.as_view(),name='list_or_create_posts'),
    path('posts/<slug>/',PostRetrieveUpdateDestroyAPIView.as_view(),name='retrieve_or_update_or_destroy_posts'),
    path('actions/star/',StarPostView.as_view()),
    path('user_active_threads/',ActiveThreadsList.as_view()),
]
