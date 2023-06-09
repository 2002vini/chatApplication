from django.shortcuts import render
from chat.models import *
import hashlib
from django.http import HttpResponse
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

def is_firebase_admin_installed():
    try:
        import firebase_admin
        return True
    except :
        return "cannot initialize app"

#def make_password(password,salt=None,hasher='default'):

def index(request):
    
    friends = Profile.objects.exclude(user=request.user)
    curr_profile_user = Profile.objects.get(user=request.user)
    params = {
        'friends': friends,
        'curr_profile_user': curr_profile_user,
    }
    
    return render(request,"index.html",params)
        
    


def chatroom(request, room_name):
    chatroom = ChatRoom.objects.get(slug=room_name)     # get the room from the id provided user_id
    messages = ChatMessage.objects.filter(room=chatroom)
    friends = Profile.objects.exclude(user=request.user)

    params = {
        "room": chatroom,
        "messages": messages,
        'friends': friends
    }
    return render(request, 'index.html', params)


def getRoomId(user_id, dm_user_id):
    room_name = ""
    if str(user_id) > str(dm_user_id):
        room_name = f"{user_id}--{dm_user_id}"
    else:
        room_name = f"{dm_user_id}--{user_id}"

    #room_id = hashlib.sha256(room_name.encode()).hexdigest()
    room_id=make_password(room_name)
    print("django has made following id:")
    print(room_id)
    return room_id,room_name


def directMessage(request, dm_user_id): 
    print("dm user id is:")
   
    logged_in_user_id = Profile.objects.get(user=request.user).unique_id 
    room_id,room_name = getRoomId(logged_in_user_id, dm_user_id)
    print("room id is:")
    print(room_id)
    print("room name is:")
    print(room_name)
    ans=False
    rooms=ChatRoom.objects.all()
    for chat_room in rooms:
        if check_password(room_name,chat_room.room_id):
            receiver=Profile.objects.get(unique_id=dm_user_id)
            chatroom=chat_room
            messages=ChatMessage.objects.filter(room=chatroom)
            friends=Profile.objects.exclude(user=request.user)
            curr_profile_user=Profile.objects.get(user=request.user)
            ans=True
            print("room primary key is:")
            print(chatroom.id)
            # print("we are in encrypted function")
            # print("receiver username is:")
            # print(receiver.user.username)
            # print("room id is")
            # print(chatroom.room_id)
            # print("messages are:")
            # print(messages)
            break
           
    if not ans:
        ChatRoom.objects.create(room_id=make_password(room_name))
        print("chatroom created")


    # if not ChatRoom.objects.filter(room_id=room_id).exists():
    #     ChatRoom.objects.create(room_id=room_id)
    # receiver=Profile.objects.get(unique_id=dm_user_id)
    # chatroom = ChatRoom.objects.get(room_id=room_id)
    # messages = ChatMessage.objects.filter(room=chatroom)
    # friends = Profile.objects.exclude(user=request.user)
    # curr_profile_user = Profile.objects.get(user=request.user)

    params = {
        'room': chatroom,
        'messages': messages,
        'friends': friends,
        'receiver':receiver,
        'curr_profile_user': curr_profile_user,
        'room_name':room_name
    }

    return render(request, 'index.html', params)
