from django.urls import path
from . import views

urlpatterns = [
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
