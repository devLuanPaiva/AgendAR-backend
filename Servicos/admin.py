from django.contrib import admin
from .models import Servicos

@admin.register(Servicos)
class ServicosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'descricao', 'estabelecimento']
    search_fields = ['nome', 'estabelecimento__nome']
