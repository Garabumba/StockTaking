# urls.py
from django.urls import path
from .views import index, get_notifications

urlpatterns = [
    path('', index, name='index'),
    path('get-notifications/', get_notifications, name='get_notifications'),
]
