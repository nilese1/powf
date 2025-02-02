from django.contrib import admin

from typing import final

from .models import Lobby
from game.models import PlayerInGame, PokerGame


@final
class PlayerInGameInline(admin.TabularInline):
    model = PlayerInGame
    extra: int = 3


@final
class PokerGameInline(admin.TabularInline):
    model = PokerGame

    inlines = [PlayerInGameInline]


@final
class LobbyAdmin(admin.ModelAdmin):
    fieldsets = []

    inlines = [PokerGameInline]

    list_display = ["lobby_name", "start_date", "is_lobby_recent"]


admin.site.register(Lobby, LobbyAdmin)
