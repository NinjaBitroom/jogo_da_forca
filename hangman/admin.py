from django.contrib import admin

from .models import Jogo, Palavra, Tema

admin.site.register(Tema)
admin.site.register(Palavra)
admin.site.register(Jogo)
