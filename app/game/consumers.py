from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import Game, QuestionState, TextAnswer
from .tasks import send_questions
from django.core.cache import cache


class GameSession(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_name = self.scope['url_route']['kwargs']['game_code']
        self.session_group_name = f'game_{self.session_name}'
        await self.channel_layer.group_add(
            self.session_group_name,
            self.channel_name,
        )
        await self.accept()
        await database_sync_to_async(self.change_player_status)(self.scope['user'], self.session_name)
        await self.channel_layer.group_send(
            self.session_group_name,
            {
                "type": "update_players",
            }
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if 'start-game' in data:
            if not await database_sync_to_async(self.is_author)():
                return
            await database_sync_to_async(self.start_game)()
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    "type": "send_categories",
                }
            )
        if 'choose-category' in data:
            if not await database_sync_to_async(self.is_author)():
                return
            category_id = int(data['choose-category'].replace('category-', ''))
            game_id = data['game-id']
            # if await database_sync_to_async(self.category_is_played)(c_id=category_id):
            #     return
            await database_sync_to_async(self.set_category_id)(category_id, game_id)
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    "type": "choose_category",
                    "category-id": category_id,
                }
            )
        if 'start-category' in data:
            if not await database_sync_to_async(self.is_author)():
                return
            # if await database_sync_to_async(self.category_is_played)(start=True):
            #     return
            await database_sync_to_async(self.change_category_status)()
            send_questions.delay(self.session_name)
        if 'get-statistics' in data:
            if not await database_sync_to_async(self.is_author)():
                return
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    "type": "send_statistics",
                }
            )
            if await database_sync_to_async(self.get_category_type)() == '1':
                send_questions.apply_async((self.session_name,), countdown=6)

        if 'player_answered' in data:
            cache_game = cache.get(self.session_name)
            cache_game -= 1
            cache.set(self.session_name, cache_game)
            if cache_game == 0:
                cache.delete(self.session_name)
                await self.channel_layer.group_send(
                    self.session_group_name,
                    {
                        "type": "change_timer"
                    }
                )
                if await database_sync_to_async(self.get_category_type)() == '1':
                    send_questions.apply_async((self.session_name,), countdown=6)

        if "correct_text_answer" in data:
            answer_id = int(data["correct_text_answer"].replace("answer-", ""))
            await database_sync_to_async(self.save_correct_text_answer)(answer_id)
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    "type": "correct_text_answer",
                    "answer_id": answer_id
                }
            )

    async def disconnect(self, code):
        await database_sync_to_async(self.change_player_status)(self.scope['user'], self.session_name, True)
        await self.channel_layer.group_discard(
            self.session_group_name,
            self.channel_name,
        )
        await self.channel_layer.group_send(
            self.session_group_name,
            {
                "type": "update_players",
            }
        )

    @staticmethod
    def set_category_id(c_id, game_id):
        game = Game.objects.get(lobby_code=game_id)
        game.current_playing_category_id = c_id
        game.save()

    def change_category_status(self):
        game = Game.objects.get(lobby_code=self.session_name)
        category = game.category_states.get(id=game.current_playing_category_id)
        category.is_played = True
        category.save()

    async def update_players(self, event):
        await self.send(text_data=json.dumps({
            "update-players": ""
        }))

    def change_player_status(self, user, session_name, disconnected=False):
        game = Game.objects.get(lobby_code=session_name)
        if self.scope['user'] != game.quiz.author:
            if user.is_authenticated:
                player = game.players.get(player=user)
            else:
                player = game.players.get(id=self.scope['session'][self.session_name])
            if disconnected:
                player.is_online = False
            elif not disconnected and not player.is_online:
                player.is_online = True
            player.save()

    async def send_question(self, event):
        question = await(database_sync_to_async(QuestionState.objects.get)(id=event['id']))
        await database_sync_to_async(self.change_question_status)(question)
        await self.send(text_data=json.dumps({
            'next-question': '',
            "update-players": "",
        }))

    async def send_categories(self, event):
        if not await database_sync_to_async(self.no_categories)():
            await self.send(text_data=json.dumps({
                "get-categories": "",
                "update-players": "",
            }))
        else:
            await database_sync_to_async(self.finish_game)()
            await self.send(text_data=json.dumps({
                "game-is-finished": "",
                "update-players": "",
            }))

    async def correct_text_answer(self, event):
        await self.send(text_data=json.dumps({
            "correct_text_answer": event["answer_id"]
        }))

    @staticmethod
    def change_question_status(q_obj):
        q_obj.is_asked = True
        q_obj.save()

    async def send_statistics(self, event):
        await self.send(text_data=json.dumps({
            "send-statistics": "send-statistics",
        }))

    async def choose_category(self, event):
        category_id = event['category-id']
        await self.send(text_data=json.dumps({
            'start-category': category_id,
        }))

    async def change_timer(self, event):
        await self.send(text_data=json.dumps({
            "change_timer": "change_timer"
        }))

    async def update_answers_block(self, event):
        await self.send(text_data=json.dumps({
            "update_answers_block": "update_answers_block"
        }))

    # def category_is_played(self, c_id=None, start=False):
    #     game = Game.objects.get(lobby_code=self.session_name)
    #     if start:
    #         category = game.category_states.get(id=game.current_playing_category_id)
    #     else:
    #         category = game.category_states.get(id=c_id)
    #     if category.category.type == '2':
    #         return False
    #     return category.is_played

    def start_game(self):
        game = Game.objects.get(lobby_code=self.session_name)
        game.start_game()

    def is_author(self):
        game = Game.objects.get(lobby_code=self.session_name)
        return game.quiz.author == self.scope['user'] or game.is_test

    def category_type_is_default(self):
        game = Game.objects.get(lobby_code=self.session_name)
        category = game.category_states.get(id=game.current_playing_category_id)
        return category.category.type == '1'

    def no_categories(self):
        game = Game.objects.get(lobby_code=self.session_name)
        return not game.category_states.filter(is_played=False).exists()

    def finish_game(self):
        game = Game.objects.get(lobby_code=self.session_name)
        game.finish_game()

    #  New
    def get_category_type(self):
        game = Game.objects.get(lobby_code=self.session_name)
        category = game.category_states.get(id=game.current_playing_category_id)
        return category.category.type

    @staticmethod
    def save_correct_text_answer(answer_id):
        answer = TextAnswer.objects.get(id=answer_id)
        points = answer.question.question.points
        player = answer.player
        player.score += points
        player.save()
