from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
    path('edit_post/<post>/',views.edit_post,name='edit_post'),
    path('delete_post/<post>/',views.delete_post,name='delete_post'),
    # path('<post>/like/',views.like_post,name='like'),
    path('<group>/<post>/',views.post_detail,name='post_detail'),
    path('<slug>/like',views.PostLikeToggle,name='like-toggle'),
    path('api/<slug>/like',views.PostLikeAPIToggle.as_view(),name='like-api-toggle'),
    path('new_post/',views.new_post,name='new_post'),
    path('search/',views.SearchView.as_view(),name='search_results'),
    path('<post>/like/',views.like_subject,name='like'),
    path('trending/',views.TrendingPage.as_view(),name='trending'),
    path('deactivate_post/<post>/',views.deactivate_post,name='deactivate_post'),
]
