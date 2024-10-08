from django.db import models
from django.contrib.auth.models import User

class Estabelecimento(models.Model):
    nome = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    email = models.EmailField()
    contato = models.CharField(max_length=12)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
