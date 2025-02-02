from .views import IndexView, lobby_view, create_lobby

from django.urls import path


app_name = "lobby"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>", lobby_view, name="lobby"),
    path("create_lobby", create_lobby, name="create_lobby"),
]
