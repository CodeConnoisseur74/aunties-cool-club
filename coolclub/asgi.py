import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount
from starlette.applications import Starlette
from chat.routing import websocket_urlpatterns
from .fastapi_app import app as fastapi_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolclub.settings")

django_asgi_app = get_asgi_application()

static_app = StaticFiles(directory="staticfiles")

application = ProtocolTypeRouter(
    {
        "http": Starlette(
            routes=[
                Mount("/static", app=static_app, name="static"),
                Mount("/", app=django_asgi_app),
                Mount("/api", app=fastapi_app),
            ]
        ),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
