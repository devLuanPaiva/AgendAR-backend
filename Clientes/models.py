from django.db import models
from django.contrib.auth.models import User

class Clientes(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    contato = models.CharField(max_length=12)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
