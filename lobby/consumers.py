import json
from typing import override
from channels.consumer import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.db.models import F

from game.models import PlayerInGame, PokerGame
from .models import Lobby


class LobbyConsumer(AsyncWebsocketConsumer):
    # async def __init__(self, *args: str | int, **kwargs: str | int) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.lobby_id: int
    #     self.lobby: Lobby
    #     self.user: User
    #     self.player: PlayerInGame
    #     self.game: PokerGame

    @database_sync_to_async
    def sync_set_attrbs(self, lobby_id: int):
        self.lobby = Lobby.objects.get(id=lobby_id)
        self.user = self.scope["user"]
        self.game = PokerGame.objects.get(lobby_id=self.lobby)

        try:
            self.player = PlayerInGame.objects.get(game_id=self.game, user_id=self.user)
            # if player is found, this must be a duplicate and so we disconnect
            _ = self.disconnect(403)
        except PlayerInGame.DoesNotExist:
            num_players = self.game.playeringame_set.count()
            is_host = num_players == 0
            self.player = PlayerInGame.objects.create(
                game_id=self.game, user_id=self.user, chips=0, is_host=is_host
            )

    @database_sync_to_async
    def is_lobby_full(self, lobby_id: int) -> bool:
        num_players = self.game.playeringame_set.count()
        max_players = self.game.max_players

        return num_players >= max_players

    @override
    async def connect(self):
        self.lobby_id: int = self.scope["url_route"]["kwargs"]["lobby_id"]
        await self.sync_set_attrbs(self.lobby_id)

        if await self.is_lobby_full(self.lobby_id):
            return

        # why did we make this async again?
        await self.channel_layer.group_add(f"lobby_{self.lobby_id}", self.channel_name)
        await self.accept()
        await self.update_player_list()

    @override
    async def disconnect(self, code: int):
        await self.close()

        if self.player.is_host:
            await self.channel_layer.group_discard(
                f"lobby_{self.lobby_id}", self.channel_name
            )
            await self.set_lobby_as_inactive()

        await self.delete_player()
        await self.update_player_list()

    @database_sync_to_async
    def set_lobby_as_inactive(self):
        self.lobby.is_active = False
        self.lobby.save()

    @database_sync_to_async
    def delete_player(self):
        _ = self.player.delete()

    async def update_player_list(self):
        message = await self.get_playerlist()

        await self.channel_layer.group_send(
            f"lobby_{self.lobby_id}",
            {
                "type": "playerlist.update",
                "message": message,
            },
        )

    @database_sync_to_async
    def get_playerlist(self):
        player_list = PlayerInGame.objects.filter(game_id=self.game).annotate(
            username=F("user_id__username")
        )

        message = []

        for player in player_list:
            message.append(
                {
                    "username": player.username,
                    "chips": player.chips,
                    "is_host": player.is_host,
                }
            )

        return message

    async def playerlist_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))
