from django.db import models
from django.contrib.auth.models import User

class Estabelecimento(models.Model):
    nome = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    numeroEndereco = models.CharField(max_length=10)
    email = models.EmailField()
    contato = models.CharField(max_length=10)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
