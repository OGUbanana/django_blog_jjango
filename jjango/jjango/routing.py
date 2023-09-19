from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from jjango.asgi import get_asgi_application
from blog.consumers import AutoWriteConsumer
from django.urls import path

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('write/', AutoWriteConsumer.as_asgi()),
        ])
    ),
})