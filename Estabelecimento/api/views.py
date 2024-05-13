from rest_framework import viewsets
from Estabelecimento.models import Estabelecimento
from .serializers import EstabelecimentoSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class EstabelecimentoViewSet(viewsets.ModelViewSet):
    queryset = Estabelecimento.objects.all()
    serializer_class = EstabelecimentoSerializer


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user        
        estabelecimento = Estabelecimento.objects.filter(usuario=user).first()
        
        if estabelecimento:
            estabelecimento_serializer = EstabelecimentoSerializer(estabelecimento)
            return Response({'estabelecimento': estabelecimento_serializer.data})
        else:
            return Response({'estabelecimento': None})