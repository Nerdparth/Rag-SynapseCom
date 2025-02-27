from django.urls import path
from .consumers import ChatroomConsumer

websocket_urlpatterns = [
    path("ws/chatroom/<str:botname>/", ChatroomConsumer.as_asgi())
]