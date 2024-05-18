from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Servicos.models import Servicos
from Servicos.api.serializers import ServicosSerializer
from Estabelecimento.models import Estabelecimento

class ServicosViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Servicos.objects.all()
    serializer_class = ServicosSerializer
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return Response({'error': 'O ID do estabelecimento é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        estabelecimento = get_object_or_404(Estabelecimento, id=estabelecimento_id)
        queryset = Servicos.objects.filter(estabelecimento=estabelecimento)
        serializer = ServicosSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Servicos.objects.all()
        servico = get_object_or_404(queryset, pk=pk)
        serializer = ServicosSerializer(servico)
        return Response(serializer.data)
    
    def create(self, request):
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
