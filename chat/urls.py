from django.urls import path
from . import views


app_name = 'chatApp'


urlpatterns = [
    path('', views.index, name="index"),
    path('<slug:room_name>/', views.chatroom, name="chatroom"),
    path('direct/<uuid:dm_user_id>/', views.directMessage, name="directMessage"),
]