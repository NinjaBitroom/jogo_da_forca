from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_tema/', views.cadastrar_tema, name='cadastrar_tema'),
    path('cadastrar_palavra/', views.cadastrar_palavra, name='cadastrar_palavra'),
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
