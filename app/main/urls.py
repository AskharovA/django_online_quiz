from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
    path('delete_sessions/', views.delete_temp_sessions, name='delete_sessions'),
    path('add_avatar/', views.add_avatar, name='add_avatar'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('check_quiz_for_errors/<int:quiz_id>/', views.check_quiz_for_errors, name='check_quiz_for_errors'),
    path('create_game_session/', views.CreateGameSessionView.as_view(), name='create_game_session'),
    path('get_avatar/<int:avatar_id>/', views.GetAvatarView.as_view(), name='get_avatar'),
    path('create_quiz/', views.CreateQuizView.as_view(), name='create_quiz'),
    path('quiz_list/', views.QuizListView.as_view(), name='quiz_list'),
    path('quiz_detail/<int:quiz_id>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('add_category/<int:quiz_id>/', views.AddCategoryView.as_view(), name='add_category'),
    path('add_question/<int:category_id>/', views.AddQuestionView.as_view(), name='add_question'),
    path('question_detail/<int:question_id>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('question_minimize/<int:question_id>/', views.QuestionMinimizeView.as_view(), name='question_minimize'),
    path('delete_question/<int:question_id>/', views.DeleteQuestionView.as_view(), name='delete_question'),
    path('add_option/<int:question_id>/', views.AddOptionView.as_view(), name='add_option'),
    path('delete_option/<int:question_id>/', views.DeleteOptionView.as_view(), name='delete_option'),
    path('category_minimize/<int:category_id>/', views.CategoryMinimizeView.as_view(), name='category_minimize'),
    path('delete_category/<int:category_id>/', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('category_full/<int:category_id>/', views.CategoryFullView.as_view(), name='category_full'),
    path('delete_quiz/<int:quiz_id>/', views.DeleteQuizView.as_view(), name='delete_quiz'),
    path('about/', views.AboutPageView.as_view(), name='about'),
]
