from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Palavra, Tema


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ["nome"]


class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ["tema", "palavra", "dica", "texto"]


class UserRegisterForm(UserCreationForm):
    group = forms.ChoiceField(
        label="Grupo",
        choices=(
            ("professores", "Professor"),
            ("alunos", "Aluno"),
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
