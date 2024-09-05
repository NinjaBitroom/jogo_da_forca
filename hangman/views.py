from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views.generic import TemplateView
from xhtml2pdf import pisa

from .forms import (
    AlunoRegisterForm,
    PalavraForm,
    ProfessorRegisterForm,
    TemaForm,
    UserRegisterForm,
)
from .models import Jogo, Palavra, Tema


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


@login_required
def cadastrar_tema(request):
    if not hasattr(request.user, "professor"):
        return HttpResponseForbidden("Você não tem permissão para cadastrar temas.")
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
        return HttpResponseForbidden("Você não tem permissão para cadastrar palavras.")
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


class IndexTemplateView(TemplateView):
    template_name = "index.html"


@login_required
def gerar_pdf(request):
    template = get_template("relatorio.html")
    jogos = Jogo.objects.all()
    context = {"jogos": jogos}
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    pisa.CreatePDF(html, dest=response)
    return response


def listar_temas(request):
    temas = Tema.objects.all()
    return render(request, "listar_temas.html", {"temas": temas})


def listar_jogos(request, tema_id):
    jogos = Jogo.objects.filter(tema_id=tema_id)
    return render(request, "listar_jogos.html", {"jogos": jogos})


@login_required
def gerar_relatorio(request):
    jogos = Jogo.objects.all()

    tema_id = request.GET.get("tema")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    if tema_id:
        jogos = jogos.filter(tema_id=tema_id)

    if data_inicio and data_fim:
        jogos = jogos.filter(data_jogada__range=[data_inicio, data_fim])

    return render(request, "relatorio.html", {"jogos": jogos})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


@login_required
def jogar(request, tema_id):
    tema = get_object_or_404(Tema, pk=tema_id)
    palavras = Palavra.objects.filter(tema=tema, professor=request.user.professor)

    import random

    palavra = random.choice(palavras) if palavras.exists() else None

    return render(
        request,
        "jogo.html",
        {"palavra": palavra.texto if palavra else "Palavra não disponível"},
    )
