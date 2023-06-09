from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        hash_value = self.room_id.split('$')[-1]
        print("hash value is:")
        print(hash_value)
        hash_value=hash_value.replace("+",'')
        hash_value=hash_value.replace("=",'')
        hash_value=hash_value.replace("/",'')
        print("modified hash value")
        print(hash_value)

        print(self.room_id)
        await self.channel_layer.group_add(
            hash_value,
            self.channel_name       # channel_name will be automatically be created for each user
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['chat_message_content']
        receiver=data['receiver_username']
        self.logged_in_user = self.scope["user"]
        hash_value = self.room_id.split('$')[-1]
        hash_value=hash_value.replace("+",'')
        hash_value=hash_value.replace("=",'')
        hash_value=hash_value.replace("/",'')
        print("we are in receiving function")
        
        await self.channel_layer.group_send(
            hash_value,
            {
                'type': 'handleChatEvent',      # name of the function that handles chat event-
                'chatMessage': message_content,
                'receiver':receiver
           
            }
        )
        await self.save_message(self.logged_in_user, self.room_id, message_content,receiver)

    async def handleChatEvent(self, event):
        chatMessage = event['chatMessage']
        receiver=event['receiver']
       
        await self.send(text_data = json.dumps({
            'message': chatMessage,   
            'receiver':receiver
            
        }))

    @sync_to_async
    def save_message(self, username, room_id, message,receiver):
        user = User.objects.get(username=username)
        print(self.logged_in_user)
        room = ChatRoom.objects.get(room_id=room_id)
        chat_obj=ChatMessage.objects.create(sender=user, room=room, message_content=message)
        ChatNotification.objects.create(chat=chat_obj,chat_sent_to=user)
        print("chat notification has been created")
        
 
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


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id=self.scope['user'].id
        self.room_group_name=f'{my_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("accepted")

    async def send_notification(self, event):
        print("send notification")
        data = json.loads(event.get('value'))
        count = data['count']
        print(event)
        await self.send(text_data=json.dumps({
            'count':count
        }))

    async def disconnect(self, code):
        print("disconnected")
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )