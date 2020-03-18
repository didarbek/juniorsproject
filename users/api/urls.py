from django.urls import path
from .views import (ProfileRetrieveAPIView, UserLoginAPIView, UserSignUpAPIView, current_user,)

urlpatterns = [
    path('login/',UserLoginAPIView.as_view(),name='users_login'),
    path('signup/',UserSignUpAPIView.as_view(),name='users_signup'),
    path('current_user/',current_user,name='current_user'),
    path('profile/<username>/',ProfileRetrieveAPIView.as_view(),name='profile_info'),
]
