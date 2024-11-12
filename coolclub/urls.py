from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Django allauth URLs
    path('chat/', include('chat.urls')),  # Chat app URLs

    # Root path redirecting to chat room list view
    path('', lambda request: redirect('list_chat_rooms'), name='home'),  # Redirect to the chat room list
]
