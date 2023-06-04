from django.urls import path
from . import views


app_name = 'chatApp'


urlpatterns = [
    path('index', views.index, name="index"),
    path('', views.home, name="home"),
    path('<slug:room_name>/', views.chatroom, name="chatroom"),
    path('direct/<uuid:dm_user_id>/', views.directMessage, name="directMessage"),
]