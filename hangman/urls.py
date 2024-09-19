from django.contrib.auth import views as auth_views
from django.urls import path

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
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("cadastrar_tema/", views.cadastrar_tema, name="cadastrar_tema"),
    path("cadastrar_palavra/", views.cadastrar_palavra, name="cadastrar_palavra"),
    path("temas/", views.listar_temas, name="listar_temas"),
    path("temas/<int:tema_id>/jogos/", views.listar_games, name="listar_jogos"),
    path("cadprofessor/", views.register_professor, name="register_professor"),
    path("cadaluno/", views.register_aluno, name="register_aluno"),
    path("relatorio/", views.gerar_relatorio, name="gerar_relatorio"),
    path("professores/", views.listar_professores, name="listar_professores"),
    path(
        "temas_por_professor/<int:professor_id>/",
        views.temas_por_professor,
        name="temas_por_professor",
    ),
    path("gerar_pdf/", views.gerar_pdf, name="gerar_pdf"),
    path("jogo_por_tema/<int:tema_id>/", views.listar_games, name="jogo_por_tema"),
]
