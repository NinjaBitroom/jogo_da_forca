from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from xhtml2pdf import pisa
from .models import Professor, Tema, Palavra, Jogo, Aluno
from .forms import TemaForm, PalavraForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import random


# Formulários de registro
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


# Registro de Professor e Aluno
def register_professor(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        professor_form = ProfessorRegisterForm(request.POST)
        if user_form.is_valid() and professor_form.is_valid():
            user = user_form.save()
            professor = professor_form.save(commit=False)
            professor.user = user
            professor.save()
            return redirect("login")
    else:
        user_form = UserRegisterForm()
        professor_form = ProfessorRegisterForm()
    return render(
        request,
        "cadprofessor.html",
        {"user_form": user_form, "professor_form": professor_form},
    )


def register_aluno(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        aluno_form = AlunoRegisterForm(request.POST)
        if user_form.is_valid() and aluno_form.is_valid():
            user = user_form.save()
            aluno = aluno_form.save(commit=False)
            aluno.user = user
            aluno.save()
            return redirect("login")
    else:
        user_form = UserRegisterForm()
        aluno_form = AlunoRegisterForm()
    return render(
        request, "cadaluno.html", {"user_form": user_form, "aluno_form": aluno_form}
    )


# Funções de login e logout
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


# Página principal (Index)
def index(request):
    professores = Professor.objects.all()
    return render(request, "index.html", {"professores": professores})


# Cadastrar Temas e Palavras
@login_required
def cadastrar_tema(request):
    if not hasattr(request.user, "professor"):
        return HttpResponse("Você não tem permissão para cadastrar temas.")
    if request.method == "POST":
        form = TemaForm(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            tema.professor = request.user.professor
            tema.save()
            return redirect("index")
    else:
        form = TemaForm()
    return render(request, "cadastrar_tema.html", {"form": form})


@login_required
def cadastrar_palavra(request):
    if not hasattr(request.user, "professor"):
        return HttpResponse("Você não tem permissão para cadastrar palavras.")
    if request.method == "POST":
        form = PalavraForm(request.POST)
        if form.is_valid():
            palavra = form.save(commit=False)
            palavra.professor = request.user.professor
            palavra.save()
            return redirect("index")
    else:
        form = PalavraForm()
    return render(request, "cadastrar_palavra.html", {"form": form})


# Funções para listagem de temas, professores e jogos
def listar_temas(request):
    temas = Tema.objects.all()
    return render(request, "listar_temas.html", {"temas": temas})


def listar_professores(request):
    professores = Professor.objects.all()
    return render(request, "listar_professores.html", {"professores": professores})


# Função para listar os jogos baseados no tema selecionado
def listar_games(request, tema_id):
    tema = get_object_or_404(Tema, pk=tema_id)
    palavras = Palavra.objects.filter(tema=tema)

    if palavras.exists():
        palavra = random.choice(palavras).palavra
    else:
        palavra = None

    return JsonResponse({"palavra": palavra})


# Geração de Relatórios e PDFs
@login_required
def gerar_relatorio(request):
    jogos = Jogo.objects.all()
    tema_id = request.GET.get("tema")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    if tema_id:
        jogos = jogos.filter(tema_id=tema_id)
    if data_inicio and data_fim:
        jogos = jogos.filter(data_jogo__range=[data_inicio, data_fim])

    return render(request, "relatorio.html", {"jogos": jogos})


@login_required
def gerar_pdf(request):
    template = get_template(
        "relatorio.html"
    )  # Certifique-se de que este template é simples
    jogos = Jogo.objects.all()  # Carregar os dados do relatório
    context = {"jogos": jogos}

    # Renderizar o template HTML
    html = template.render(context)

    # Preparar a resposta do PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio.pdf"'

    # Gerar o PDF usando xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar se houve erros ao gerar o PDF
    if pisa_status.err:
        return HttpResponse("Erro ao gerar o PDF", status=500)

    return response


# Função para selecionar temas por professor
def temas_por_professor(request, professor_id):
    temas = Tema.objects.filter(professor_id=professor_id)
    temas_data = [{"id": tema.id, "nome": tema.nome} for tema in temas]
    return JsonResponse({"temas": temas_data})
