from typing import final, override

from django.contrib.auth.models import AbstractUser, AnonymousUser, User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from game.models import PlayerInGame, PokerGame
from lobby.forms import LobbyForm
from .models import Lobby

from django.views.generic import ListView, TemplateView
from django.utils import timezone
from django.db.models import F, Count


def is_lobby_full(lobby: Lobby) -> bool:
    game: PokerGame = PokerGame.objects.get(id=lobby.pokergame.pk)
    is_full = game.max_players > PlayerInGame.objects.filter(game_id=game).count()

    return is_full


@final
class IndexView(ListView):
    model = Lobby
    template_name: str = "lobby/index.html"

    @override
    def get_context_data(self, **kwargs: str):
        context = super().get_context_data(**kwargs)

        context["lobby_list"] = (
            Lobby.objects.filter(
                start_date__lte=timezone.now(),
                is_active=True,
            )
            .annotate(num_players=Count("pokergame__playeringame"))
            .annotate(max_players=F("pokergame__max_players"))
            .filter(num_players__lt=F("max_players"))
            .order_by("-start_date")[:10]
        )

        return context


def lobby_view(request: HttpRequest, pk: int) -> HttpResponse:
    context = {}

    lobby_id: int = pk
    lobby: Lobby = Lobby.objects.get(id=pk)
    context["lobby_id"] = lobby_id

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authentication:login"))

    elif not lobby.is_lobby_recent() or not lobby.is_active:
        messages.error(request, "Lobby is expired or invalid")
        return HttpResponseRedirect(reverse("lobby:index"))

    elif not is_lobby_full(lobby):
        messages.error(request, "Lobby is full")
        return HttpResponseRedirect(reverse("lobby:index"))

    return render(request, "lobby/lobby.html", context)


def create_lobby(request: HttpRequest):
    """Handles the lobby creation form"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authentication:login"))

    # if we're getting a POST, create the lobby, otherwise return the form html
    if request.method == "POST":
        form = LobbyForm(request.POST)
        if form.is_valid():
            lobby = form.save()
            return HttpResponseRedirect(reverse("lobby:lobby", args=(lobby.pk,)))
    else:
        form = LobbyForm()

    return render(request, "lobby/index.html", {"form": form})
