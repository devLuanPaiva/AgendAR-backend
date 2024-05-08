from rest_framework import viewsets
from Clientes.models import Clientes
from .serializers import ClientesSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer