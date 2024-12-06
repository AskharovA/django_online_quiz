from celery import shared_task
from app.game.models import Game
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache


@shared_task
def send_questions(session_name):
    channel_layer = get_channel_layer()
    game = Game.objects.get(lobby_code=session_name)
    category = game.category_states.get(id=game.current_playing_category_id)
    questions = category.question_states.filter(is_asked=False)
    players_count = game.players.count()
    cache.set(session_name, players_count, 900)
    cache.set(session_name + "_answers", [], 900)
    if questions.exists():
        question = questions.first()
        async_to_sync(channel_layer.group_send)(
            f'game_{session_name}',
            {
                'type': 'send_question',
                'id': question.id,
            }
        )
    else:
        async_to_sync(channel_layer.group_send)(
            f'game_{session_name}',
            {
                'type': 'send_categories',
            }
        )
