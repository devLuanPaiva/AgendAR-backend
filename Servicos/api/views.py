from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from Servicos.models import Servicos
from Servicos.api.serializers import ServicosSerializer

class ServicosViews(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ServicosSerializer(data=request.data)
        if serializer.is_valid():
            nome = serializer.validated_data['nome']
            valor = serializer.validated_data['valor']
            descricao = serializer.validated_data['descricao']
            estabelecimento = serializer.validated_data['estabelecimento']
            
            if Servicos.objects.filter(nome=nome, estabelecimento=estabelecimento).exists():
                return Response({'error': 'Este serviço já está cadastrado neste estabelecimento.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if valor <= 0:
                return Response({'error': 'O valor do serviço deve ser maior que zero.'}, status=status.HTTP_400_BAD_REQUEST)
            
            servico = Servicos(nome=nome, valor=valor, descricao=descricao, estabelecimento=estabelecimento)
            servico.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)