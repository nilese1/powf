import datetime
from typing import final

from django.db import models
from django.db.models.fields import BooleanField, CharField, DateField, DateTimeField
from django.utils import timezone
from django.contrib import admin
from django.db.models import Count


@final
class Lobby(models.Model):
    lobby_name: CharField[str] = CharField(max_length=20)
    start_date: DateField[datetime.datetime] = DateTimeField(
        "date started", auto_now=True
    )
    is_active: BooleanField[bool] = BooleanField(default=True)

    @admin.display(boolean=True, ordering="start_date", description="Is Lobby Recent")
    def is_lobby_recent(self) -> bool:
        # we do not allow lobbys to be active for more than 1 day
        is_recent: bool = (
            timezone.now()
            >= self.start_date
            >= timezone.now() - datetime.timedelta(days=1)
        )

        return is_recent
