from typing import override
from django import forms
from django.core import validators

from game.models import PokerGame

from .models import Lobby


class LobbyForm(forms.ModelForm):
    max_players: forms.IntegerField = forms.IntegerField(label="Max Players")

    class Meta:
        model: type = Lobby
        fields: list[str] = ["lobby_name"]

    @override
    def save(self, commit: bool = True) -> Lobby:
        lobby: Lobby = super().save(commit=commit)

        max_players: int = self.cleaned_data["max_players"]
        if commit:
            _ = PokerGame.objects.create(lobby_id=lobby, max_players=max_players)

        return lobby
