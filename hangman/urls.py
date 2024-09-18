from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("cadastrar_tema/", views.TemaCreateView.as_view(), name="cadastrar_tema"),
    path(
        "temas/<int:pk>/atualizar/",
        views.TemaUpdateView.as_view(),
        name="atualizar_tema",
    ),
    path(
        "cadastrar_palavra/",
        views.PalavraCreateView.as_view(),
        name="cadastrar_palavra",
    ),
    path("jogo/<int:tema_id>/", views.JogoView.as_view(), name="jogo"),
    path(
        "temas/<int:tema_id>/jogos/", views.JogosListView.as_view(), name="listar_jogos"
    ),
    path("relatorio/", views.RelatorioView.as_view(), name="gerar_relatorio"),
    path("pdf/", views.PdfView.as_view(), name="pdf"),
]
