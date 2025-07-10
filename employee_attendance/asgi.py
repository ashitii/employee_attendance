import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_attendance.settings')
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chatting.routing # This import is now safe as apps are ready.

application = ProtocolTypeRouter({
    "http": django_asgi_app, # Use the pre-initialized Django ASGI app for HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatting.routing.websocket_urlpatterns
        )
    ),
})