from django.urls import re_path
from .consumers import LobbyConsumer

websocket_urlpatterns = [
    # Websocket url for a given lobby id (ws/lobby/<lobby_id>)
    re_path(r"ws/lobby/(?P<lobby_id>\w+)/$", LobbyConsumer.as_asgi()),
]
