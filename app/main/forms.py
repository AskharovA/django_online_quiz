from django.forms import (ModelForm, CharField, TextInput, Textarea, ImageField, FileInput, FileField, ChoiceField,
                          Select, ModelChoiceField)
from .models import Quiz, Category, Question, Option

from app.game.models import Game, PlayerAvatar


class QuizForm(ModelForm):
    title = CharField(required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название игры',
        'autocomplete': 'off',
    }))
    description = CharField(required=True, widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Описание игры',
        'autocomplete': 'off',
    }))

    class Meta:
        model = Quiz
        fields = ('title', 'description')


class CategoryForm(ModelForm):
    name = CharField(required=True, widget=TextInput(attrs={
        'class': 'form-control add-category-input',
        'placeholder': 'Название категории',
        'autocomplete': 'off',
    }))
    type = ChoiceField(required=True, choices=Category.Type.choices, widget=Select(attrs={
        'class': 'form-select'
    }))

    class Meta:
        model = Category
        fields = ('name', 'type')


class QuestionForm(ModelForm):
    points = CharField(required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    text = CharField(required=True, widget=Textarea(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    image = ImageField(required=False, widget=FileInput(attrs={
        'class': 'form-control'
    }))
    audio = FileField(required=False, widget=FileInput(attrs={
        'class': 'form-control'
    }))
    video = FileField(required=False, widget=FileInput(attrs={
        'class': 'form-control'
    }))
    correct_text_answer = CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))

    class Meta:
        model = Question
        fields = ('points', 'text', 'audio', 'image', 'correct_text_answer', 'video')


class OptionForm(ModelForm):
    text = CharField(required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))

    class Meta:
        model = Option
        fields = ('text', 'is_correct')


class GameSessionForm(ModelForm):
    quiz = ModelChoiceField(queryset=Quiz.objects.none(),required=True,widget=Select(attrs={
        'class': 'home-input'
    }))
    timer = CharField(required=True,widget=TextInput(attrs={
        'class': 'home-input',
        'autocomplete': 'off',
    }))
    text_answer_timer = CharField(required=True, widget=TextInput(attrs={
        'class': 'home-input',
        'autocomplete': 'off',
    }))

    class Meta:
        model = Game
        fields = ('quiz', 'timer', 'text_answer_timer')

    def __init__(self, *args, author=None, **kwargs):
        super(GameSessionForm, self).__init__(*args, **kwargs)
        if author:
            self.fields['quiz'].queryset = Quiz.objects.filter(author=author)


class AddAvatarForm(ModelForm):
    image = ImageField(required=True, widget=FileInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = PlayerAvatar
        fields = ('image', )
