from django import template
from app.game.models import Game
from django.db.models import Q

register = template.Library()


@register.simple_tag()
def get_active_game_sessions(user):
    return Game.objects.filter(Q(quiz__author=user) & (Q(status=Game.Status.ACTIVE) | Q(status=Game.Status.WAITING)))
