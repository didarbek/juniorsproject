from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
    path('delete_post/<post>/',views.delete_post,name='delete_post'),
    path('<group>/<post>/',views.post_detail,name='post_detail'),
    path('<post>/like/',views.like_post,name='like'),
    path('new_post/',views.new_post,name='new_post'),
    path('edit_post/<post>/',views.edit_post,name='edit_post'),
]
