import datetime

from .models import Lobby
from game.models import PokerGame, PlayerInGame

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User


def create_lobby(
    date_created: datetime.date, name: str = "test", active: bool = True
) -> Lobby:

    lobby = Lobby.objects.create(
        lobby_name=name, start_date=date_created, is_active=active
    )

    game = PokerGame.objects.create(lobby_id=lobby)

    return lobby


def add_players(lobby: Lobby, num_players: int) -> list[PlayerInGame]:
    players: list[PlayerInGame] = []

    for i in range(num_players):
        user = User(username="test" + str(i), password="test")
        player = PlayerInGame(
            game_id=lobby.pokergame, user_id=user, chips=0, is_host=False
        )
        user.save()
        player.save()

    return players


class LobbyIndexViewTests(TestCase):
    def test_no_lobbies(self):
        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lobbies are available")
        self.assertQuerySetEqual(response.context["lobby_list"], [])

    def test_inactive_lobby(self):
        inactive_lobby = create_lobby(timezone.now(), active=False)
        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lobbies are available")
        self.assertQuerySetEqual(response.context["lobby_list"], [])

    def test_future_lobby(self):
        future_time: datetime.date = timezone.now() + datetime.timedelta(seconds=1)
        future_lobby = create_lobby(future_time, active=False)
        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lobbies are available")
        self.assertQuerySetEqual(response.context["lobby_list"], [])

    def test_active_lobby(self):
        active_lobby = create_lobby(timezone.now(), active=True)
        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["lobby_list"], [active_lobby])

    def test_two_active_lobbies(self):
        active_lobby1 = create_lobby(timezone.now(), active=True)
        active_lobby2 = create_lobby(
            timezone.now() - datetime.timedelta(hours=1), active=True
        )
        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["lobby_list"], [active_lobby1, active_lobby2]
        )

    def test_empty_lobby(self):
        empty_lobby: Lobby = create_lobby(timezone.now(), active=True)

        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0/9")

    def test_three_player_lobby(self):
        three_player_lobby: Lobby = create_lobby(timezone.now(), active=True)
        three_players: list[PlayerInGame] = add_players(three_player_lobby, 3)

        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3/9")

    def test_full_lobby(self):
        full_lobby: Lobby = create_lobby(timezone.now(), active=True)
        full_players: list[PlayerInGame] = add_players(full_lobby, 9)

        response: HttpResponse = self.client.get(reverse("lobby:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lobbies are available")
