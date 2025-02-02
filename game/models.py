from datetime import datetime
from django.db.models.fields import BooleanField, DateTimeField, IntegerField
from django.db.models.fields.related import ForeignKey
from lobby.models import Lobby
from django.contrib.auth.models import User

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .settings import MAXIMUM_PLAYERS_PER_GAME


class PokerGame(models.Model):
    lobby_id: models.OneToOneField[Lobby] = models.OneToOneField(
        Lobby, on_delete=models.CASCADE, null=False
    )

    max_players: IntegerField[int] = models.IntegerField(
        default=MAXIMUM_PLAYERS_PER_GAME,
        validators=[
            MaxValueValidator(
                MAXIMUM_PLAYERS_PER_GAME,
                f"Maximum players must be less than {MAXIMUM_PLAYERS_PER_GAME}",
            ),
            MinValueValidator(2, f"Must have at least 2 players"),
        ],
        null=False,
        blank=False,
    )

    start_time: DateTimeField[datetime] = models.DateTimeField(
        name="start time", auto_now=True
    )
    end_time: DateTimeField[datetime | None] = models.DateTimeField(
        name="end time", null=True
    )


class PlayerInGame(models.Model):
    game_id: ForeignKey[PokerGame] = models.ForeignKey(
        PokerGame, on_delete=models.CASCADE
    )
    user_id: ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)
    chips: IntegerField[int] = models.IntegerField(
        validators=[MinValueValidator(0, "Chips must be a positive value")],
        null=False,
        blank=False,
    )
    is_host: BooleanField[bool] = models.BooleanField()
    last_active: DateTimeField[datetime] = models.DateTimeField(auto_now=True)


class GameResults(models.Model):
    game_id: ForeignKey[PokerGame] = models.ForeignKey(
        PokerGame, on_delete=models.CASCADE
    )
    winner_id: ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)
    winning_amount: IntegerField[int] = models.IntegerField()
