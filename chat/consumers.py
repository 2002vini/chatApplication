from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name       # channel_name will be automatically be created for each user
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['chat_message_content']
        self.logged_in_user = self.scope["user"]

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'handleChatEvent',      # name of the function that handles chat event-
                'chatMessage': message_content,
            }
        )
        await self.save_message(self.logged_in_user, self.room_id, message_content)

    async def handleChatEvent(self, event):
        chatMessage = event['chatMessage']
        await self.send(text_data = json.dumps({
            'message': chatMessage,
        }))

    @sync_to_async
    def save_message(self, username, room_id, message):
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(room_id=room_id)
        ChatMessage.objects.create(sender=user, room=room, message_content=message)



class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "online_users_pool"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        status = data['status']
        logged_in_user = self.scope["user"]
        await self.setUserStatus(logged_in_user, status)

    @sync_to_async
    def setUserStatus(self, username, status):
        user = User.objects.get(username=username)
        profile_user = Profile.objects.get(user=user)
        if status == 'online':
            profile_user.online_status = True
            profile_user.save()
        else:
            profile_user.online_status = False
            profile_user.save()
