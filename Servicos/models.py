from django.db import models

class Servicos(models.Model):
    nome = models.CharField(max_length=150)
    valor = models.FloatField()
    descricao = models.CharField(max_length=200)
    estabelecimento = models.ForeignKey('Estabelecimento.Estabelecimento', on_delete=models.CASCADE)