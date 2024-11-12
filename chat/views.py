# chat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def send_message(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    error, message = None, None
    if request.user not in chat_room.members.all():
        error = "Unauthorized"

    text = request.POST.get('text')
    if not text:
        error = "Message is empty"

    if error is not None:
        message = Message.objects.create(chat_room=chat_room, sender=request.user, text=text)

    return render(request, 'chat/_message.html', {'error': error, 'message': message})


def redirect_to_chat(request):
    return redirect('list_chat_rooms')

from django.shortcuts import render

def home(request):
    return render(request, 'chat/home.html')

@login_required
def create_chat_room(request):
    if request.method == "POST":
        name = request.POST.get("name")
        chat_room = ChatRoom.objects.create(name=name)
        chat_room.members.add(request.user)

        return redirect("chat_room", chat_room_id=chat_room.id)
    return render(request, "chat/create_chat_room.html")

@login_required
def join_chat_room(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    chat_room.members.add(request.user)
    return redirect("chat_room", chat_room_id=chat_room.id)

@login_required
def leave_chat_room(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    chat_room.members.remove(request.user)
    return redirect("chat_home")

@login_required
def list_chat_rooms(request):
    user_chatrooms = request.user.chatrooms.all()
    return render(request, "chat/chat_room_list.html", {"chatrooms": user_chatrooms})

@login_required
def chat_room(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user not in chat_room.members.all():
        return redirect("list_chat_rooms")

    messages = chat_room.messages.all()
    return render(request, "chat/chat_room.html", {"chat_room": chat_room, "messages": messages})
