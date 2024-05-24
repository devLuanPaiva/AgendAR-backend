from django.db import models
from Estabelecimento.models import Estabelecimento
from Clientes.models import Clientes
from Servicos.models import Servicos
from Horarios.models import Horario


class AgendamentosPeloCliente(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servicos, on_delete=models.CASCADE)
    horario_selecionado = models.TimeField()
    dia_selecionado = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    
class AgendamentosPeloEstabelecimento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30)
    contato = models.CharField(max_length=12) 
    servico = models.ForeignKey(Servicos, on_delete=models.CASCADE)
    horario_selecionado = models.TimeField()
    dia_selecionado = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)