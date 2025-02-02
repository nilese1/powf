from django.urls import re_path
from .consumers import LobbyConsumer

websocket_urlpatterns = [
    re_path(r"ws/lobby/(?P<lobby_id>\w+)/$", LobbyConsumer.as_asgi()),
]
