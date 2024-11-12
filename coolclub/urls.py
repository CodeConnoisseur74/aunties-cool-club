from django.contrib import admin
from django.urls import path, include
from chat import views as chat_views  # Import views from chat app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('chat.urls')),

    # Use the redirect view for the root URL
    path('', chat_views.redirect_to_chat, name='home'),
]
