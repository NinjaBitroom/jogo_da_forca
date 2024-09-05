from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Aluno, Palavra, Professor, Tema


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ["nome"]


class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ["tema", "palavra", "dica", "texto"]


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=100)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ProfessorRegisterForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ["nome"]


class AlunoRegisterForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome"]
