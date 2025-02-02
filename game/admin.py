from typing import final
from django.contrib import admin

from .models import PlayerInGame


@final
class PlayerInGameAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = [
        "user_id__username",
        "game_id__lobby_id__lobby_name",
        "chips",
        "is_host",
        "last_active",
    ]


admin.site.register(PlayerInGame, PlayerInGameAdmin)
