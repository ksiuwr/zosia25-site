from django.db import models
from django.utils.translation import gettext_lazy as _
from server.users.models import User


class Boardgame(models.Model):
    name = models.CharField(verbose_name=_(
        "Name of the boardgame"), max_length=200)
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    url = models.CharField(verbose_name=_(
        "Url to boardgamegeek.com"), max_length=200)

    def __str__(self):
        return self.name

    def toggle_accepted(self):
        self.accepted = not self.accepted
        self.save()


class Vote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    boardgame = models.ForeignKey(
        Boardgame,
        on_delete=models.CASCADE,
        related_name="boardgame_votes"
    )
