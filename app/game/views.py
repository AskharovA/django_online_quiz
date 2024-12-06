import uuid
from django.shortcuts import render, redirect, reverse
from .models import Game, QuestionState, PlayerStat, TextAnswer, PlayerAvatar, generate_code_for_game
from app.main.models import Option, Quiz
from django.views.decorators.http import require_POST
from django.core.cache import cache


def main(request, game_code: str):
    game = Game.objects.get(lobby_code=game_code)
    return render(request, 'game/game.html', {
        'game': game,
    })


def join_game(request):
    if request.method == 'POST':
        game_code = request.POST['game_code']
        game = Game.objects.filter(lobby_code=game_code)
        if not game.exists():
            return redirect(reverse('main:index'))
        game = game.first()
        if 'player_name' in request.POST:
            if game_code in request.session:
                player = PlayerStat.objects.get(game=game, id=request.session[game_code])
                if player.player_name != request.POST['player_name']:
                    player.player_name = request.POST['player_name']
                    player.save()
            else:
                player_names = [player.player_name for player in PlayerStat.objects.filter(game=game)]
                if request.POST['player_name'] in player_names:
                    player_name = request.POST['player_name'] + str(uuid.uuid4())[:5]
                else:
                    player_name = request.POST['player_name']
                player = PlayerStat.objects.get_or_create(game=game, player_name=player_name)[0]
                request.session[game_code] = player.id
        else:
            player = PlayerStat.objects.get_or_create(
                game=game,
                player=request.user,
                player_name=request.user.profile.nickname
            )[0]
        if not request.user.is_authenticated:
            avatar_id = int(request.POST['avatar_id'])
            avatar = PlayerAvatar.objects.filter(id=avatar_id)
            if avatar.exists():
                player.avatar = avatar.first()
            else:
                avatar = PlayerAvatar.objects.first()
                player.avatar = avatar
            player.save()
        return redirect(reverse('game:game', args=[request.POST['game_code']]))
    return redirect(reverse('main:index'))


def run_test_game(request):
    quiz = Quiz.objects.get(for_test=True)
    lobby_code = generate_code_for_game()
    game = Game.objects.create(quiz=quiz, is_test=True, lobby_code=lobby_code)
    player_name = "test_" + str(uuid.uuid4())[:2]
    player = PlayerStat.objects.create(game=game, player_name=player_name)
    request.session[lobby_code] = player.id
    avatar = PlayerAvatar.objects.all().first()
    player.avatar = avatar
    player.save()

    return redirect(reverse('game:game', args=[lobby_code]))


def update_players(request, game_id):
    game = Game.objects.get(id=game_id)
    players = game.players.order_by('-score')
    return render(request, 'game/includes/players.html', {
        'players': players,
    })


def get_categories(request, game_id):
    game = Game.objects.get(id=game_id)
    categories = game.category_states.all()
    return render(request, 'game/includes/categories.html', {
        'categories': categories,
    })


def play_category(request, game_id):
    game = Game.objects.get(id=game_id)
    current_category = game.category_states.get(id=game.current_playing_category_id)
    question = current_category.question_states.filter(is_asked=True).last()
    if current_category.category.type == '1':
        return render(request, 'game/includes/question.html', {
            'question': question,
        })
    elif current_category.category.type == '2':
        return render(request, 'game/includes/text_question.html', {
            'question': question,
        })


def check_player_answer(request, option_id, question_id):
    question = QuestionState.objects.get(id=question_id)
    game = question.game
    if request.user.is_authenticated:
        player = PlayerStat.objects.get(game=game, player=request.user)
    else:
        player = PlayerStat.objects.get(id=request.session[game.lobby_code])

    players_cache = cache.get(game.lobby_code + "_answers")
    players_cache.append(player)

    option = Option.objects.get(id=option_id)
    cache.set(game.lobby_code + "_answers", players_cache, 900)

    if option.is_correct:
        player.score += question.question.points
        player.save()
    option_state = game.option_states.get(option=option)
    option_state.answers.add(player)
    return render(request, 'game/includes/player_answer.html', {
        'options': question.option_states.all(),
        'player_option': option_state,
    })


def get_statistics(request, game_id):
    game = Game.objects.get(id=game_id)
    current_category = game.category_states.get(id=game.current_playing_category_id)
    question = current_category.question_states.filter(is_asked=True).last()
    if current_category.category.type == '1':
        return render(request, 'game/includes/statistics.html', {
            'options': question.option_states.all(),
            'question': question,
        })
    return render(request, 'game/includes/player_text_answers.html', {
        'question': question,
    })


@require_POST
def save_player_text_answer(request, question_id):
    question = QuestionState.objects.get(id=question_id)
    game = question.game
    if request.user.is_authenticated:
        player = game.players.get(player=request.user)
    else:
        player = game.players.get(id=request.session[game.lobby_code])

    players_cache = cache.get(game.lobby_code + "_answers")
    players_cache.append(player)
    cache.set(game.lobby_code + "_answers", players_cache, 900)

    answer = request.POST['text-answer']
    TextAnswer.objects.create(
        game=game,
        player=player,
        question=question,
        answer=answer
    )
    return render(request, 'game/includes/accept_text_answer.html')


def correct_text_answer(request):
    # answer = TextAnswer.objects.get(id=answer_id)
    # points = answer.question.question.points
    # player = answer.player
    # player.score += points
    # player.save()
    return render(request, 'game/includes/correct_answer.html')


def send_final_statistic(request, game_id):
    game = Game.objects.get(id=game_id)
    players_ordered = game.players.order_by('-score')
    if players_ordered.exists():
        max_score = players_ordered.first().score
        winners = players_ordered.filter(score=max_score)
    else:
        winners = players_ordered
    return render(request, 'game/includes/final_statistics.html', {
        'players': players_ordered,
        'winners': winners,
    })


def close_game(request, game_id):
    game = Game.objects.get(id=game_id)
    game.finish_game()
    game.save()
    return redirect(reverse('main:index'))


def update_answers_block(request, game_id):
    game = Game.objects.get(id=game_id)
    players_cache = cache.get(game.lobby_code + "_answers")
    return render(request, 'game/includes/answers_block.html', {
        'players': players_cache
    })
