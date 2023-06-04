from django.shortcuts import render
from chat.models import *
import hashlib


def index(request):
    friends = Profile.objects.exclude(user=request.user)
    params = {
        'friends': friends
    }
    return render(request, "chatApp/index2.html", params)

def home(request):
    rooms = ChatRoom.objects.all()
    params = {
        'chatrooms': rooms,
    }
    return render(request, 'chatApp/home.html', params)


def chatroom(request, room_name):
    chatroom = ChatRoom.objects.get(slug=room_name)     # get the room from the id provided user_id
    messages = ChatMessage.objects.filter(room=chatroom)
    friends = Profile.objects.exclude(user=request.user)

    params = {
        "room": chatroom,
        "messages": messages,
        'friends': friends
    }
    return render(request, 'chatApp/room.html', params)


def getRoomId(user_id, dm_user_id):
    room_name = ""
    if str(user_id) > str(dm_user_id):
        room_name = f"{user_id}--{dm_user_id}"
    else:
        room_name = f"{dm_user_id}--{user_id}"

    room_id = hashlib.sha256(room_name.encode()).hexdigest()
    return room_id


def directMessage(request, dm_user_id): 
    logged_in_user_id = Profile.objects.get(user=request.user).unique_id 
    room_id = getRoomId(logged_in_user_id, dm_user_id)

    if not ChatRoom.objects.filter(room_id=room_id).exists():
        ChatRoom.objects.create(room_id=room_id)

    chatroom = ChatRoom.objects.get(room_id=room_id)
    messages = ChatMessage.objects.filter(room=chatroom)
    friends = Profile.objects.exclude(user=request.user)
   
    params = {
        'room': chatroom,
        'messages': messages,
        'friends': friends
    }

    return render(request, 'chatApp/room.html', params)
