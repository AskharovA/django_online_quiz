from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, CategoryState, QuestionState, Category, Question, OptionState


@receiver(post_save, sender=Game)
def create_game_states(sender, instance, created, **kwargs):
    if created:
        categories = Category.objects.filter(quiz=instance.quiz)
        for category in categories:
            category_state = CategoryState.objects.create(game=instance, category=category)
            for question in category.questions.all():
                question_state = QuestionState.objects.create(game=instance, category=category_state, question=question)
                for option in question.options.all():
                    OptionState.objects.create(game=instance, question=question_state, option=option)
