from django.contrib import admin
from .models import Estabelecimento

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado', 'email', 'contato']
    search_fields = ['nome', 'cidade']