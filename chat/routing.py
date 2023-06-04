from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/direct/<str:room_id>/', consumers.ChatConsumer.as_asgi()),       # .as_asgi is done cause our ChatConsumer is an asynchronous function
    path('ws/status/', consumers.OnlineConsumer.as_asgi()),
]  


