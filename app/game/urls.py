from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('join_game/', views.join_game, name='join_game'),
path('run_test_game/', views.run_test_game, name='run_test_game'),
    path('close_game/<int:game_id>/', views.close_game, name='close_game'),
    path('finish_game/<int:game_id>/', views.send_final_statistic, name='finish_game'),
    path('correct_text_answer/', views.correct_text_answer, name='correct_text_answer'),
    path('save_player_text_answer/<int:question_id>/', views.save_player_text_answer, name='save_player_text_answer'),
    path('get_statistics/<int:game_id>/', views.get_statistics, name='get-statistics'),
    path('player_answer/<int:option_id>/<int:question_id>/', views.check_player_answer, name='player-answer'),
    path('play_category/<int:game_id>/', views.play_category, name='play-category'),
    path('get_categories/<int:game_id>/', views.get_categories, name='get_categories'),
    path('update_players/<int:game_id>/', views.update_players, name='update_players'),
    path('update_answers_block/<int:game_id>/', views.update_answers_block, name='update_answers_block'),
    path('<str:game_code>/', views.main, name='game'),
]
