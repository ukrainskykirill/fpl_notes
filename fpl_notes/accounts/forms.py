from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from notes.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="e-mail")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Повтор пароля")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль")
