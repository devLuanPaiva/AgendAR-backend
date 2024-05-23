from rest_framework import viewsets,status
from Clientes.models import Clientes
from .serializers import ClientesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user        
        cliente = Clientes.objects.filter(usuario=user).first()
        
        if cliente:
            cliente_serializer = ClientesSerializer(cliente)
            return Response({'cliente': cliente_serializer.data})
        else:
            return Response({'cliente': None})