from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['login', 'email', 'password1', 'password2', "telegram_id"]

    def clean_login(self):
        login = self.cleaned_data['login']
        if CustomUser.objects.filter(login=login).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return login

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)