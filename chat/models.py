from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="chatrooms")
    admins = models.ManyToManyField(User, related_name="admin_chatrooms")
    video_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    parent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="children"
    )


class Message(models.Model):
    POST = "post"
    MESSAGE = "message"
    LESSON = "lesson"

    MESSAGE_TYPE_CHOICES = [
        (POST, "Post"),
        (MESSAGE, "Message"),
        (LESSON, "Lesson"),
    ]

    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    media = models.ImageField(upload_to="chat_media/", null=True, blank=True)
    message_type = models.CharField(
        max_length=10, choices=MESSAGE_TYPE_CHOICES, default=MESSAGE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"

    class Meta:
        ordering = ["-created_at"]


class Invitation(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined"),
    ]

    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="invitations"
    )
    invited_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invitations"
    )
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invitations"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invited_user.username} invited to {self.chat_room.name}"
