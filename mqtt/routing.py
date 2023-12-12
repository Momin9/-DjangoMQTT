from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from mqtt.consumers import MyMqttConsumer


application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/some_path/", MyMqttConsumer.as_asgi()),
                ]
            )
        ),
    }
)
