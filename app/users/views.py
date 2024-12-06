from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class RegistrationView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(self.request, user)
        return redirect(reverse('main:index'))


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/includes/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserLogoutView(LogoutView):
    pass
