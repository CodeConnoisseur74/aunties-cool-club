from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_chat_rooms, name="list_chat_rooms"),
    path("create/", views.create_chat_room, name="create_chat_room"),
    path("<int:chat_room_id>/", views.chat_room, name="chat_room"),
    path("<int:chat_room_id>/join/", views.join_chat_room, name="join_chat_room"),
    path("<int:chat_room_id>/leave/", views.leave_chat_room, name="leave_chat_room"),
    path("<int:chat_room_id>/send/", views.send_message, name="send_message"),
    path("chat/<int:chat_room_id>/invite/", views.invite_user, name="invite_user"),
    path(
        "chat/<int:chat_room_id>/request-invite/",
        views.request_invite,
        name="request_invite",
    ),
    path(
        "chat/<int:chat_room_id>/manage-invitations/",
        views.manage_invitations,
        name="manage_invitations",
    ),
]
