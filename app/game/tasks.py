from celery import shared_task
from app.game.models import Game
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_questions(session_name):
    channel_layer = get_channel_layer()
    game = Game.objects.get(lobby_code=session_name)
    category = game.category_states.get(id=game.current_playing_category_id)
    questions = category.question_states.filter(is_asked=False)
    if questions.exists():
        question = questions.first()
        async_to_sync(channel_layer.group_send)(
            f'game_{session_name}',
            {
                'type': 'send_question',
                'id': question.id,
            }
        )
        if category.category.type == '1':
            send_questions.apply_async((session_name, ), countdown=category.game.timer + 7)
    else:
        async_to_sync(channel_layer.group_send)(
            f'game_{session_name}',
            {
                'type': 'send_categories',
            }
        )
#
#
# @shared_task
# def delete_finished_games():
#     time_threshold = timezone.now() - timedelta(days=1)
#     finished_games = Game.objects.filter(
#         status=Game.Status.FINISHED,
#         created__lt=time_threshold,
#     )
#     if finished_games.exists():
#         finished_games.delete()
