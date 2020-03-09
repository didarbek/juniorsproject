from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('show_reports/<group>/',views.show_reports,name='show_reports'),
    path('report_post/<post>/',views.report_post,name='report_post'),
    path('report_comment/<pk>/',views.report_comment,name='report_comment'),
]