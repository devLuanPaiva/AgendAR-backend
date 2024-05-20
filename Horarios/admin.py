from django.contrib import admin
from .models import Horario, TempoHorario

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('estabelecimento', 'dia_da_semana', 'turno', 'horario_inicio', 'horario_fim')
    list_filter = ('estabelecimento', 'dia_da_semana', 'turno')

@admin.register(TempoHorario)
class TempoHorarioAdmin(admin.ModelAdmin):
    list_display = ('tempo',)
