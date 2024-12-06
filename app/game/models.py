from django.db import models
from app.main.models import Quiz, User, Category, Question, Option
from string import ascii_lowercase, ascii_uppercase, digits
from random import sample


def generate_code_for_game():
    code = ''.join(sample(ascii_uppercase + ascii_lowercase + digits, 10))
    return code


class Game(models.Model):
    class Status(models.TextChoices):
        WAITING = 'W', 'Waiting for players'
        ACTIVE = 'A', 'Game is active'
        FINISHED = 'F', 'Game is finished'

    quiz = models.ForeignKey(Quiz, related_name='games', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.WAITING)
    timer = models.PositiveSmallIntegerField(default=10)
    text_answer_timer = models.PositiveIntegerField(default=30)
    lobby_code = models.CharField(max_length=29, default=generate_code_for_game)
    current_playing_category_id = models.IntegerField(null=True, blank=True)

    is_test = models.BooleanField(default=False)

    def start_game(self):
        self.status = self.Status.ACTIVE
        self.save()

    def finish_game(self):
        self.status = self.Status.FINISHED
        self.save()

    def __str__(self):
        return f'{self.quiz.author.profile.nickname} - {self.quiz.title}'

    class Meta:
        verbose_name = 'игровая сессия'
        verbose_name_plural = 'игровые сессий'


class PlayerAvatar(models.Model):
    image = models.ImageField(upload_to='images/game/avatars/')

    def __str__(self):
        return self.image.name


class PlayerStat(models.Model):
    player = models.ForeignKey(User, related_name='stats', on_delete=models.CASCADE, blank=True, null=True)
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    is_online = models.BooleanField(default=True)
    player_name = models.CharField(max_length=25, blank=True, null=True)
    avatar = models.ForeignKey(PlayerAvatar, blank=True, null=True, on_delete=models.DO_NOTHING)

    def update_score(self, value):
        if isinstance(value, int):
            self.score = value
            self.save()

    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'


class CategoryState(models.Model):
    game = models.ForeignKey(Game, related_name='category_states', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='states', on_delete=models.CASCADE)
    is_played = models.BooleanField(default=False)

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = 'состояние категории'
        verbose_name_plural = 'состояние категорий'


class QuestionState(models.Model):
    game = models.ForeignKey(Game, related_name='question_states', on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryState, related_name='question_states', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, related_name='states', on_delete=models.CASCADE)
    is_asked = models.BooleanField(default=False)
    current = models.BooleanField(default=False)

    def get_question_count(self):
        return self.category.question_states.filter(is_asked=True).count()

    def get_total_questions_count(self):
        return self.category.question_states.count()

    def __str__(self):
        return self.question.text

    class Meta:
        verbose_name = 'состояние вопроса'
        verbose_name_plural = 'состояние вопросов'


class OptionState(models.Model):
    game = models.ForeignKey(Game, related_name='option_states', on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionState, related_name='option_states', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='states', on_delete=models.CASCADE)
    answers = models.ManyToManyField(PlayerStat)

    def __str__(self):
        return self.option.text

    class Meta:
        verbose_name = 'состояние варианта ответа'
        verbose_name_plural = 'состояние вариантов ответа'


class TextAnswer(models.Model):
    game = models.ForeignKey(Game, related_name='text_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionState, related_name='text_answers', on_delete=models.CASCADE)
    player = models.ForeignKey(PlayerStat, related_name='text_answers', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.question.text

    class Meta:
        verbose_name = 'устный ответ'
        verbose_name_plural = 'устные ответы'
