from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns
from .fastapi_app import app as fastapi_app  # Import FastAPI app

application = ProtocolTypeRouter(
    {
        "http": fastapi_app,  # Route HTTP requests to FastAPI directly
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns  # WebSocket routing
            )
        ),
    }
)
