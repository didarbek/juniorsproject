from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('',views.inbox,name='inbox'),
    path('<username>/',views.messages,name='messages'),
    path('send/',views.send,name='send_message'),
    path('delete/',views.delete,name='delete_message'),
    path('check/',views.check,name='check_message'),
    path('load_new_messages/',views.load_new_messages,name='load_new_messages'),
    path('load_last_twenty_messages/',views.load_last_twenty_messages,name='load_last_twenty_messages'),
]
