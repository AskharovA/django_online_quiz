from django.contrib import admin
from .models import Quiz, Category, Question, Option


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ...


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    ...