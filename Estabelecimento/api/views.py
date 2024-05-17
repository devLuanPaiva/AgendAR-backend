from rest_framework import viewsets, status
from Estabelecimento.models import Estabelecimento
from .serializers import EstabelecimentoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class EstabelecimentoViewSet(viewsets.ModelViewSet):
    queryset = Estabelecimento.objects.all()
    serializer_class = EstabelecimentoSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        if not all(data.values()):
            return Response({"error": "Todos os campos devem ser preenchidos."}, status=status.HTTP_400_BAD_REQUEST)

        if Estabelecimento.objects.filter(nome=data['nome']).exists():
            return Response({"error": "Este estabelecimento já está cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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