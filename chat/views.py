from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message, Invitation
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string


def my_htmx_view(request):
    if request.headers.get("HX-Request"):
        return HttpResponse("<div>HTMX content</div>")
    return HttpResponse("<div>Non-HTMX content</div>")


def home_view(request):
    return render(request, "home.html")


@login_required
@require_POST
def send_message(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user not in chat_room.members.all():
        return HttpResponse({"error": "Unauthorized"}, status=403)

    text = request.POST.get("text", "").strip()
    message_type = request.POST.get("message_type", Message.MESSAGE)

    if not text:
        return HttpResponse({"error": "Message cannot be empty."}, status=400)

    message = Message.objects.create(
        chat_room=chat_room, sender=request.user, text=text, message_type=message_type
    )

    html = render_to_string("chat/_message.html", {"message": message})
    return HttpResponse(html)


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
        return HttpResponse({"error": "Unauthorized"}, status=403)

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

    if request.user not in chat_room.members.all():
        return redirect("list_chat_rooms")

    messages = chat_room.messages.order_by("created_at")

    if message_type := request.GET.get("message_type", None) is not None:
        messages = messages.filter(message_type=message_type)

    return render(
        request, "chat/chat_room.html", {"chat_room": chat_room, "messages": messages}
    )


@login_required
def parent_dashboard(request):
    children = request.user.children.all()

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
        return HttpResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        video_link = request.POST.get("video_link")
        chat_room.video_link = video_link
        chat_room.save()

    return redirect("chat_room", chat_room_id=chat_room.id)


@login_required
def invite_user(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user not in chat_room.admins.all():
        messages.error(
            request, "You are not authorized to invite users to this chat room."
        )
        return redirect("chat_room", chat_room_id=chat_room.id)

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        Invitation.objects.create(
            chat_room=chat_room, invited_user=user, invited_by=request.user
        )

        messages.success(request, f"Invitation sent to {user.username} successfully!")
        return redirect("chat_room", chat_room_id=chat_room.id)

    return render(
        request,
        "chat/invite_user.html",
        {"chat_room": chat_room, "users": User.objects.exclude(chatrooms=chat_room)},
    )


@login_required
def request_invite(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user in chat_room.members.all():
        return HttpResponse({"error": "You are already a member."}, status=400)

    existing_request = Invitation.objects.filter(
        chat_room=chat_room, invited_user=request.user, status=Invitation.PENDING
    ).first()

    if existing_request:
        return HttpResponse({"error": "You already requested an invite."}, status=400)

    Invitation.objects.create(
        chat_room=chat_room,
        invited_user=request.user,
        invited_by=None,
        status=Invitation.PENDING,
    )

    return HttpResponse("Invite request sent successfully!", status=200)


@login_required
def manage_invitations(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

    if request.user not in chat_room.admins.all():
        return HttpResponse({"error": "Unauthorized"}, status=403)

    pending_invitations = chat_room.invitations.filter(status=Invitation.PENDING)

    if request.method == "POST":
        invitation_id = request.POST.get("invitation_id")
        action = request.POST.get("action")

        invitation = get_object_or_404(
            Invitation, id=invitation_id, chat_room=chat_room
        )

        if action == Invitation.ACCEPTED:
            invitation.status = Invitation.ACCEPTED
            chat_room.members.add(invitation.invited_user)
        elif action == Invitation.DECLINED:
            invitation.status = Invitation.DECLINED

        invitation.save()

        return redirect("manage_invitations", chat_room_id=chat_room.id)

    return render(
        request,
        "chat/manage_invitations.html",
        {
            "chat_room": chat_room,
            "invitations": pending_invitations,
            "ACCEPTED": Invitation.ACCEPTED,  # Pass constants
            "DECLINED": Invitation.DECLINED,  # Pass constants
        },
    )
