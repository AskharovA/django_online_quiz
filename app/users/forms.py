from django.forms import ModelForm, CharField, TextInput, PasswordInput, EmailField, ImageField, FileInput, ValidationError
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate


class RegisterForm(UserCreationForm):
    email = EmailField(required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email',
        'autocomplete': 'off',
    }))
    password1 = CharField(required=True, widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'пароль',
        'autocomplete': 'off',
    }))
    password2 = CharField(required=True, widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'подтверждение пароля',
        'autocomplete': 'off',
    }))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = EmailField(required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email',
        'autocomplete': 'off',
    }))
    password = CharField(required=True, widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'пароль',
        'autocomplete': 'off',
    }))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise ValidationError('Пожалуйста, введите корректный Email и пароль.')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ProfileForm(ModelForm):
    avatar = ImageField(widget=FileInput(attrs={
        'class': 'form-control',
    }))
    nickname = CharField(widget=TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Profile
        fields = ['avatar', 'nickname']
