from django.contrib import admin
from django.urls import path, include
from chat.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("chat/", include("chat.urls")),
    path("", home_view, name="home"),
]
