from typing import final

from .models import PokerGame, PlayerInGame

from django.views.generic import TemplateView


@final
class GameIndexView(TemplateView):
    template_name = "game/index.html"


@final
class GamePlayView(TemplateView):
    template_name = "game/play.html"
