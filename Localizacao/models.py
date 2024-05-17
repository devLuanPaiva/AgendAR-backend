from django.db import models

class Localicazao(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    estabelecimento = models.ForeignKey('Estabelecimento.Estabelecimento', on_delete=models.CASCADE)