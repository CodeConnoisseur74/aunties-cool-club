# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_chat_rooms, name='list_chat_rooms'),  # List of chat rooms (home page for chat)
    path('create/', views.create_chat_room, name='create_chat_room'),  # Create a new chat room
    path('<int:chat_room_id>/', views.chat_room, name='chat_room'),  # Chat room by ID
    path('<int:chat_room_id>/join/', views.join_chat_room, name='join_chat_room'),  # Join a specific chat room
    path('<int:chat_room_id>/leave/', views.leave_chat_room, name='leave_chat_room'),  # Leave a specific chat room
]
