from django.contrib import admin
from .models import CustomUser, ConnectionRequest, ChatMessage

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ConnectionRequest)
admin.site.register(ChatMessage)
