import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from xhtml2pdf import pisa

from .forms import (
    PalavraForm,
    TemaForm,
    UserRegisterForm,
)
from .models import Jogo, Palavra, Tema


class IndexListView(ListView):
    template_name = "index.html"
    model = Tema


class UserCreateView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        group = get_object_or_404(Group, name=form.cleaned_data["group"])
        user = form.save()
        user.groups.add(group)
        return super().form_valid(form)


class TemaCreateView(PermissionRequiredMixin, CreateView):
    model = Tema
    form_class = TemaForm
    template_name = "cadastrar_tema.html"
    success_url = reverse_lazy("index")
    permission_required = "hangman.add_tema"

    def form_valid(self, form):
        form.instance.professor = self.request.user
        return super().form_valid(form)


class TemaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Tema
    form_class = TemaForm
    template_name = "atualizar_tema.html"
    success_url = reverse_lazy("index")
    permission_required = "hangman.change_tema"


class PalavraCreateView(PermissionRequiredMixin, CreateView):
    model = Palavra
    form_class = PalavraForm
    template_name = "cadastrar_palavra.html"
    success_url = reverse_lazy("index")
    permission_required = "hangman.add_palavra"

    def form_valid(self, form):
        form.instance.professor = self.request.user
        return super().form_valid(form)


@login_required
def gerar_pdf(request):
    template = get_template("relatorio.html")
    jogos = Jogo.objects.all()
    context = {"jogos": jogos}
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    pisa.CreatePDF(html, dest=response)
    return response


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

    palavra = random.choice(palavras) if palavras.exists() else None

    return render(
        request,
        "jogo.html",
        {"palavra": palavra.texto if palavra else "Palavra não disponível"},
    )
