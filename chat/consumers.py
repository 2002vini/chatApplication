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
        message = data['message']
        username = data['username']

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'handleChatEvent',      # name of the function that handles chat event-
                'chatMessage': message,
                'username': username,
            }
        )
        await self.save_message(username, self.room_id, message)

    async def handleChatEvent(self, event):
        message = event['chatMessage']
        username = event['username']
        await self.send(text_data = json.dumps({
            'type': 'chat',
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room_id, message):
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(room_id=room_id)
        ChatMessage.objects.create(sender=user, room=room, message_content=message)
