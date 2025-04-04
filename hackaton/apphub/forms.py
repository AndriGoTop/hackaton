from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.utils.safestring import mark_safe


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['login', 'email', 'password1', 'password2', "telegram_id"]

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if CustomUser.objects.filter(login=login).exists():
            msg = mark_safe(
                'Пользователь с таким логином уже существует. '
                '<a href="login/">Войти</a>')
            raise forms.ValidationError(msg)
        return login

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            msg = mark_safe(
                'Пользователь с такой почтой уже зарегистрирован. '
                '<a href="login/">Войти</a>'
            )
            raise forms.ValidationError(msg)
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
