from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class ConnectionRequest(models.Model):
    connection_sender = models.ForeignKey(CustomUser, related_name='connection_sender', on_delete=models.CASCADE)
    connection_receiver = models.ForeignKey(CustomUser, related_name='connection_receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'connection_sender', 'connection_receiver')  # Ensure unique requests between sender and receiver


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)