from django.urls import path
from .views import HomePostView, PostDetailView
app_name = 'posts'

urlpatterns = [
    path('', HomePostView.as_view(), name='all_post'),
    path('<slug>/', PostDetailView.as_view(), name='post_detail')

]

