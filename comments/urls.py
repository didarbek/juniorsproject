from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('delete_comment/<pk>/',views.delete_comment,name='delete_comment'),
]
