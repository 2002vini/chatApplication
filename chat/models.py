from django.db import models
from django.contrib.auth.models import User

import uuid


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    image = models.FileField(upload_to='profile_pic', null=True)
    last_text = models.CharField(max_length=100)
    online_status = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, null=True)
    room_id = models.CharField(max_length=64)       # storing sha256 string


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at',]

class ChatNotification(models.Model):
    chat=models.ForeignKey(ChatMessage,on_delete=models.CASCADE)
    chat_sent_to=models.ForeignKey(User,on_delete=models.CASCADE)
    is_seen=models.BooleanField(default=False)