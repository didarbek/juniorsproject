from django.urls import path
from .views import delete_comment,deactivate_comment

app_name = 'comments'

urlpatterns = [
    path('delete_comment/<int:pk>/',delete_comment, name='delete_comment'),
    path('deactivate_comment/<pk>/',deactivate_comment,name='deactivate_comment'),
]
