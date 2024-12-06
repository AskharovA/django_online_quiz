from django.contrib import admin
from .models import Game, PlayerStat, CategoryState, QuestionState, OptionState, TextAnswer, PlayerAvatar


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    ...


@admin.register(PlayerStat)
class PlayerStatAdmin(admin.ModelAdmin):
    ...


@admin.register(CategoryState)
class CategoryStateAdmin(admin.ModelAdmin):
    ...


@admin.register(QuestionState)
class QuestionStateAdmin(admin.ModelAdmin):
    list_display = ['game', 'category', 'question', 'is_asked', 'current']
    list_editable = ['is_asked', 'current']


@admin.register(OptionState)
class OptionStateAdmin(admin.ModelAdmin):
    ...


@admin.register(TextAnswer)
class TextAnswerAdmin(admin.ModelAdmin):
    ...


@admin.register(PlayerAvatar)
class PlayerAvatarAdmin(admin.ModelAdmin):
    ...