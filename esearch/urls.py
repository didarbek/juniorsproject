from django.urls import path
from . import views

app_name = 'esearch'

urlpatterns = [
    path('esearch/',views.search_index,name='search_view'),    
]
