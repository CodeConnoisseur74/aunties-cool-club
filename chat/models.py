# chat/models.py
from django.db import models
from django.contrib.auth.models import User


# ChatRoom model - to handle multiple rooms, but minimal setup for now
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="chatrooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Message model - to store each chat message
class Message(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    media = models.ImageField(
        upload_to="chat_media/", null=True, blank=True
    )  # Optional media field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"

    class Meta:
        ordering = ["-created_at"]  # Order messages by latest first


