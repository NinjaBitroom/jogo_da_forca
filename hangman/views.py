from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from xhtml2pdf import pisa

from .forms import (
    PalavraForm,
    TemaForm,
    UserRegisterForm,
)
from .models import Jogo, Palavra, Tema


class UserCreateView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        group = get_object_or_404(Group, name=form.cleaned_data["group"])
        user = form.save()
        user.groups.add(group)
        return super().form_valid(form)


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
