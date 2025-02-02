from .views import GameIndexView, GamePlayView

from django.urls import path


app_name = "game"
urlpatterns = [
    path("<int:pk>/", GameIndexView.as_view(), name="index"),
    path("<int:pk>/play/", GamePlayView.as_view(), name="play"),
]
