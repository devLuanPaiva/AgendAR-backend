from django.contrib import admin
from .models import AgendamentosPeloCliente, AgendamentosPeloEstabelecimento

@admin.register(AgendamentosPeloEstabelecimento)
class AgendamentoEstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('estabelecimento', 'servico', 'nome', 'horario_selecionado', 'dia_selecionado')
    list_filter = ('estabelecimento', 'servico', 'nome', )
    
@admin.register(AgendamentosPeloCliente)
class AgendamentoClienteAdmin(admin.ModelAdmin):
    list_display = ('estabelecimento', 'servico', 'cliente', 'horario_selecionado', 'dia_selecionado')
    list_filter = ('estabelecimento', 'servico', 'cliente', )