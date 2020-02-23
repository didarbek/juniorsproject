from django.urls import path
from .views import UserSubscriptionListPage
urlpatterns = [
    path('sub-user/', UserSubscriptionListPage.as_view(), name='sub_user'),

]
