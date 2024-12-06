from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import QuizForm, CategoryForm, QuestionForm, OptionForm, GameSessionForm, AddAvatarForm
from .models import Quiz, Category, Question, Option
from app.game.models import PlayerAvatar, PlayerStat, Game
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.generic.base import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from datetime import timedelta
from django.utils import timezone


@method_decorator(require_POST, name='dispatch')
class BasePostOnlyView(LoginRequiredMixin, View):
    pass


class MainPageView(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['main/home_auth.html']
        else:
            return ['main/home_no_auth.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            avatars = PlayerAvatar.objects.all()
            current_avatar = PlayerAvatar.objects.all().first()
            context['avatars'] = avatars
            context['current_avatar'] = current_avatar
        return context


class GetAvatarView(DetailView):
    model = PlayerAvatar
    template_name = 'main/includes/current_avatar.html'
    context_object_name = 'avatar'
    pk_url_kwarg = 'avatar_id'


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'main/quiz_list.html'
    context_object_name = 'quiz_objects'

    def get_queryset(self):
        return Quiz.objects.filter(author=self.request.user)


class CreateQuizView(LoginRequiredMixin, CreateView):
    form_class = QuizForm
    template_name = 'main/create_quiz.html'
    success_url = reverse_lazy('main:quiz_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'main/quiz_detail.html'
    pk_url_kwarg = 'quiz_id'
    context_object_name = 'quiz'

    def get(self, request, *args, **kwargs):
        quiz_object = self.get_object()
        if quiz_object.author != self.request.user:
            return redirect(reverse_lazy('main:index'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm()
        return context


class QuestionMinimizeView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'main/includes/question_mini.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'


class QuestionDetailView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'main/includes/question_full.html'
    pk_url_kwarg = 'question_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_form'] = self.get_form()
        question = self.get_object()
        if question.category.quiz.author != self.request.user:
            return redirect(reverse('main:index'))

        context['option_forms'] = [
            OptionForm(
                instance=option,
                prefix=f'option_{i}'
            ) for i, option in enumerate(question.options.all(), start=1)
        ]
        return context

    def form_valid(self, form):
        with transaction.atomic():
            question = form.save()
            options = question.options.all()

            for i, option in enumerate(options, start=1):
                option_form = OptionForm(self.request.POST, instance=option, prefix=f'option_{i}')
                if not option_form.is_valid():
                    return self.form_invalid(form)
                option_form.save()

            return render(self.request, 'main/messages/message.html', {
                'message': 'Изменения успешно сохранены',
                'status': 'success',
            })

    def form_invalid(self, form):
        return render(self.request, 'main/messages/message.html', {
            'message': 'Ошибки в форме',
            'status': 'error',
        })


@method_decorator(require_POST, name='dispatch')
class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/includes/category_full.html'

    def form_valid(self, form):
        category = form.save(commit=False)
        category.quiz = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        category.save()

        return render(self.request, self.template_name, {'category': category})


class AddQuestionView(BasePostOnlyView):
    template_name = 'main/includes/question_mini.html'

    def post(self, request, category_id):
        category = Category.objects.get(id=category_id)
        question = Question.objects.create(category=category, text='Новый вопрос', points=100)
        if category.type == '1':
            for _ in range(4):
                question.options.create(text='')
        return render(request, self.template_name, {'question': question})


class AddOptionView(BasePostOnlyView):
    template_name = 'main/includes/option_list.html'

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        if question.options.count() < 6:
            Option.objects.create(text='', question=question)
        options = question.options.all()
        option_forms = [OptionForm(instance=option, prefix=f'option_{i}') for i, option in enumerate(options, start=1)]
        return render(request, self.template_name, {'option_forms': option_forms})


class DeleteOptionView(BasePostOnlyView):
    template_name = 'main/includes/option_list.html'

    def post(self, request, question_id):
        question = Question.objects.get(id=question_id)
        options = question.options.all()
        if options.exists() and question.options.count() > 2:
            options.last().delete()
        option_forms = [OptionForm(instance=option, prefix=f'option_{i}') for i, option in enumerate(options, start=1)]

        return render(request, self.template_name, {
            'option_forms': option_forms
        })


class CategoryMinimizeView(LoginRequiredMixin, DetailView):
    model = Category
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'
    template_name = 'main/includes/category_mini.html'


class CategoryFullView(LoginRequiredMixin, DetailView):
    model = Category
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'
    template_name = 'main/includes/category_full.html'


class DeleteQuestionView(BasePostOnlyView):
    template_name = 'main/includes/category_full.html'

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        category = question.category
        question.delete()
        return render(request, self.template_name, {'category': category})


class DeleteCategoryView(BasePostOnlyView):
    template_name = 'main/messages/message.html'

    def post(self, request, category_id):
        category = Category.objects.get(id=category_id)
        category.delete()
        return render(request, self.template_name, {
            'message': 'Категория удалена',
            'status': 'success',
        })


class DeleteQuizView(BasePostOnlyView):
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if quiz.author == self.request.user:
            quiz.delete()
            return redirect(reverse('main:quiz_list'))


class CreateGameSessionView(LoginRequiredMixin, CreateView):
    form_class = GameSessionForm
    template_name = 'game/create_game_session.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs

    def get_initial(self):
        return {'timer': 10, 'text_answer_timer': 30}

    def form_valid(self, form):
        game = form.save()
        return redirect(reverse('game:game', args=[game.lobby_code]))

    def form_invalid(self, form):
        return redirect(reverse('main:create_game_session'))


class AboutPageView(TemplateView):
    template_name = 'main/about.html'


def check_quiz_for_errors(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    from .tools import check_quiz_for_errors
    errors = check_quiz_for_errors(quiz)
    return render(request, 'main/messages/quiz_errors.html', {
        'errors_count': errors['errors'],
        'errors_message': errors['message'],
    })


def admin_panel(request):
    form = AddAvatarForm()
    return render(request, 'main/admin_panel.html', {'form': form})


def add_avatar(request):
    form = AddAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect(reverse('main:admin_panel'))


def delete_temp_sessions(request):
    time_threshold = timezone.now() - timedelta(days=1)
    finished_games = Game.objects.filter(
        status=Game.Status.FINISHED,
        created__lt=time_threshold,
    )
    if finished_games.exists():
        finished_games.delete()
    return redirect(reverse('main:index'))
