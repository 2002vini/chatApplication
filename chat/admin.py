from django.contrib import admin
from .models import *


class CustomChatRoom(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'room_id']

class CustomChatMessage(admin.ModelAdmin):
    list_display = ['id', 'sender', 'room', 'created_at', 'message_content']

class CustomProfile(admin.ModelAdmin):
    list_display = ['user', 'unique_id']

class CustomChatNotification(admin.ModelAdmin):
    list_display=['chat','chat_sent_to','is_seen']


admin.site.register(Profile, CustomProfile)
admin.site.register(ChatRoom, CustomChatRoom)
admin.site.register(ChatMessage, CustomChatMessage)
admin.site.register(ChatNotification,CustomChatNotification)


