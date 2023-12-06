from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/game/<str:game_code>/', consumers.GameSession.as_asgi()),
]