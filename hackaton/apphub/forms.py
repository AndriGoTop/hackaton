from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'picture', 'telegram_id']


class CustomUserRegistrationForm(UserCreationForm):
    # telegram_input = forms.CharField(required=False, label="Telegram ID")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'telegram_id']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.telegram_id = self.cleaned_data['telegram_id']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
