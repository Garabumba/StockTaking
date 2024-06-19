from django.db import models

class Notification(models.Model):
    message = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)