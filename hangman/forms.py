from django import forms
from .models import Tema, Palavra

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nome']

class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['tema', 'palavra', 'dica', 'texto']

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)