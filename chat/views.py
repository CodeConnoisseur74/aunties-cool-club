# chat/views.py

from django.shortcuts import render, redirect  # For rendering templates and redirecting
from django.contrib.auth.decorators import login_required  # To ensure views are only accessible to logged-in users
from django.contrib.auth.models import User  # Django's built-in User model
from .models import ChatRoom, Message  # Importing the models we've created


from django.shortcuts import render

def home(request):
    return render(request, 'chat/home.html')  # Or redirect to list_chat_rooms if desired



@login_required
def create_chat_room(request):
    if request.method == "POST":
        name = request.POST.get("name")
        members = request.POST.getlist("members")  # Assuming you have a multi-select form field for members
        chat_room = ChatRoom.objects.create(name=name)
        chat_room.members.add(request.user)  # Add the creator as a member
        chat_room.members.add(*members)  # Add selected members
        return redirect("chat_room", chat_room_id=chat_room.id)

    # Render a form to create a chat room with a list of possible members
    return render(request, "chat/create_chat_room.html", {"users": User.objects.all()})

@login_required
def join_chat_room(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    chat_room.members.add(request.user)
    return redirect("chat_room", chat_room_id=chat_room.id)

@login_required
def leave_chat_room(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    chat_room.members.remove(request.user)
    return redirect("chat_home")  # Redirect to chat room list or home page

@login_required
def list_chat_rooms(request):
    user_chatrooms = request.user.chatrooms.all()  # Accessing through the related_name
    return render(request, "chat/chat_room_list.html", {"chatrooms": user_chatrooms})

@login_required
def chat_room(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    
    # Check if the user is a member of the chat room
    if request.user not in chat_room.members.all():
        return redirect("list_chat_rooms")  # Redirect non-members to the room list

    # Otherwise, allow the user to view the chat room
    messages = chat_room.messages.all()
    return render(request, "chat/chat_room.html", {"chat_room": chat_room, "messages": messages})

