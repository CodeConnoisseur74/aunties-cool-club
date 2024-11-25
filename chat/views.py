# chat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from allauth.account.views import LoginView


@csrf_exempt
def my_login_view(request):
    return LoginView.as_view()(request)


@login_required
@require_POST
def send_message(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    # Check if the user is a member of the chat room
    if request.user not in chat_room.members.all():
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Get message data from the POST request
    text = request.POST.get("text", "").strip()
    message_type = request.POST.get(
        "message_type", Message.MESSAGE
    )  # Default to "MESSAGE"

    # Validate message content
    if not text:
        return JsonResponse({"error": "Message cannot be empty."}, status=400)

    # Create the message
    message = Message.objects.create(
        chat_room=chat_room, sender=request.user, text=text, message_type=message_type
    )

    # Render the message using the partial template
    html = render_to_string("chat/_message.html", {"message": message})
    return JsonResponse({"html": html})


@login_required
def create_chat_room(request):
    if request.method == "POST":
        name = request.POST.get("name")
        admin_ids = request.POST.getlist("admins")
        chat_room = ChatRoom.objects.create(name=name)
        chat_room.members.add(request.user)
        chat_room.admins.add(request.user)

        if admin_ids:
            chat_room.admins.add(*User.objects.filter(id__in=admin_ids))

        return redirect("chat_room", chat_room_id=chat_room.id)

    return render(request, "chat/create_chat_room.html", {"users": User.objects.all()})


def redirect_to_chat(request):
    return redirect("list_chat_rooms")


@login_required
def remove_member(request, chat_room_id, user_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user not in chat_room.admins.all():
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user_to_remove = get_object_or_404(User, id=user_id)
    chat_room.members.remove(user_to_remove)

    return redirect("chat_room", chat_room_id=chat_room_id)


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

    # Ensure the user is a member of the chat room
    if request.user not in chat_room.members.all():
        return redirect("list_chat_rooms")

    # Get filter criteria from the request (optional)
    message_type = request.GET.get("message_type", None)

    # Fetch messages based on type or fetch all
    if message_type:
        messages = chat_room.messages.filter(message_type=message_type)
    else:
        messages = chat_room.messages.all()

    return render(
        request, "chat/chat_room.html", {"chat_room": chat_room, "messages": messages}
    )


@login_required
def parent_dashboard(request):
    # Get all children of the logged-in parent
    children = request.user.children.all()

    # Fetch chat rooms that the children are part of
    chatrooms = ChatRoom.objects.filter(members__in=[child.id for child in children])

    return render(
        request,
        "chat/parent_dashboard.html",
        {"chatrooms": chatrooms, "children": children},
    )


@login_required
def set_video_link(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user not in chat_room.admins.all():
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        video_link = request.POST.get("video_link")
        chat_room.video_link = video_link
        chat_room.save()

    return redirect("chat_room", chat_room_id=chat_room.id)


def load_history(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    messages = chat_room.messages.order_by("-created_at")[:50]  # Load last 50 messages
    return render(request, "chat/_history.html", {"messages": messages})
