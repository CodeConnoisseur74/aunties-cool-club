from django.contrib import admin

from .models import ChatRoom

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    filter_horizontal = ('members', 'admins')
    list_filter = ('created_at',)
