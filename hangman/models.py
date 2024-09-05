from django.contrib.auth.models import User
from django.db import models


class Tema(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Palavra(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    palavra = models.CharField(max_length=100)
    dica = models.TextField(blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.palavra


class Jogo(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    data_jogo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.first_name} - {self.tema.nome} - {self.data_jogo}"
