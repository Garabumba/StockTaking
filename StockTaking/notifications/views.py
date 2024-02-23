from django.shortcuts import render
from .models import Notification

def index(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    return render(request, 'notifications/index.html', {'notifications': notifications})

# views.py
from django.http import JsonResponse

def get_notifications(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    return JsonResponse({'notifications': [{'message': n.message} for n in notifications]})
