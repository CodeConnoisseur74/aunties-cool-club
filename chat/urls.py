# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_chat_rooms, name='list_chat_rooms'),
    path('create/', views.create_chat_room, name='create_chat_room'),
    path('<int:chat_room_id>/', views.chat_room, name='chat_room'),
    path('<int:chat_room_id>/join/', views.join_chat_room, name='join_chat_room'),
    path('<int:chat_room_id>/leave/', views.leave_chat_room, name='leave_chat_room'),
    path('<int:chat_room_id>/send/', views.send_message, name='send_message'),
]
