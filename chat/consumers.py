import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.accept()

        messages = await self.get_chat_history()
        for message in messages:
            await self.send(text_data=json.dumps({
                "message": message.text,
                "sender": message.sender.username,  # Use username for serialization
                "timestamp": message.created_at.isoformat(),
            }))

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender = data['sender']

        await self.save_message(sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, sender, content):
        from django.contrib.auth.models import User
        from .models import ChatRoom, Message
        with transaction.atomic():
            room = ChatRoom.objects.get(id=self.room_id)
            user = User.objects.get(username=sender)
            Message.objects.create(chat_room=room, sender=user, text=content)

    @database_sync_to_async
    def get_chat_history(self):
        from .models import Message
        with transaction.atomic():
            return list(
                Message.objects.filter(chat_room__id=self.room_id)
                .select_related("sender")
                .order_by("created_at")
            )
