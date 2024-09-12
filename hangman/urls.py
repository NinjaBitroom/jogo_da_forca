from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("cadastrar_tema/", views.TemaCreateView.as_view(), name="cadastrar_tema"),
    path("cadastrar_palavra/", views.cadastrar_palavra, name="cadastrar_palavra"),
    path("temas/<int:tema_id>/jogos/", views.listar_jogos, name="listar_jogos"),
    path("relatorio/", views.gerar_relatorio, name="gerar_relatorio"),
]
