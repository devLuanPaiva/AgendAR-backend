from django.db import models
from Estabelecimento.models import Estabelecimento

class Horario(models.Model):
    DIA_DA_SEMANA_CHOICES = [
        ('SEGUNDA', 'Segunda-feira'),
        ('TERCA', 'Terça-feira'),
        ('QUARTA', 'Quarta-feira'),
        ('QUINTA', 'Quinta-feira'),
        ('SEXTA', 'Sexta-feira'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    TURNO_DO_HORARIO = [
        ('MANHA', 'Manhã'),
        ('TARDE', 'Tarde'),
        ('NOITE', 'Noite'),
    ]
    dia_da_semana = models.CharField(max_length=10, choices=DIA_DA_SEMANA_CHOICES)
    turno = models.CharField(max_length=10, choices=TURNO_DO_HORARIO)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    
    class Meta: 
        unique_together =  ('dia_da_semana', 'turno', 'horario_inicio', 'horario_fim', 'estabelecimento', 'id')
    def __str__(self):
        return f"{self.estabelecimento} - {self.dia_da_semana} - {self.turno} ({self.horario_inicio} - {self.horario_fim})"

class TempoHorario(models.Model):
    tempo = models.DurationField()