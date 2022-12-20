from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email


class AuthForm(AuthenticationForm):
    username = forms.EmailField(
        label='Почта',
        validators=[validate_email],
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
