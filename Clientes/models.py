from django.db import models
from django.contrib.auth.models import User

class Clientes(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    contato = models.CharField(max_length=10)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
