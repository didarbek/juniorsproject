from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('activities/',views.ActivitiesPage.as_view(),name='activities'),    
    path('activities/check/',views.check_activities,name='check_activities'),
]
