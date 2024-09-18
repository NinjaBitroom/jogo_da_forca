import random

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        palavras = Palavra.objects.filter()
        qtd_palavras = {}
        for palavra in palavras:
            if palavra.tema not in qtd_palavras:
                qtd_palavras[palavra.tema] = 0
            qtd_palavras[palavra.tema] += 1
        context["qtd_palavras"] = qtd_palavras
        return context


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


class JogoView(TemplateView):
    template_name = "jogo.html"

    def get_context_data(self, **kwargs):
        tema = get_object_or_404(Tema, pk=self.kwargs["tema_id"])
        palavras = Palavra.objects.filter(tema=tema)
        palavra = random.choice(palavras) if palavras.exists() else None
        Jogo.objects.create(
            user=self.request.user if not self.request.user.is_anonymous else None,
            tema=tema,
        )
        return {"palavra": palavra.texto if palavra else "Palavra não disponível"}


class JogosListView(ListView):
    model = Jogo
    template_name = "listar_jogos.html"
    context_object_name = "jogos"

    def get_queryset(self):
        return super().get_queryset().filter(tema_id=self.kwargs["tema_id"])


class RelatorioView(TemplateView):
    template_name = "relatorio.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        jogos = Jogo.objects.all()

        tema_id = self.request.GET.get("tema")
        data_inicio = self.request.GET.get("data_inicio")
        data_fim = self.request.GET.get("data_fim")

        if tema_id:
            jogos = jogos.filter(tema_id=tema_id)

        if data_inicio and data_fim:
            jogos = jogos.filter(data_jogo__range=[data_inicio, data_fim])

        ctx["jogos"] = jogos
        ctx["data_inicio"] = data_inicio
        ctx["data_fim"] = data_fim
        return ctx


class PdfView(View):
    def get(self, request):
        template = get_template("relatorio.html")
        jogos = Jogo.objects.all()
        context = {
            "jogos": jogos,
            "data_inicio": request.GET.get("data_inicio"),
            "data_fim": request.GET.get("data_fim"),
        }
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        pisa.CreatePDF(html, dest=response)
        return response
