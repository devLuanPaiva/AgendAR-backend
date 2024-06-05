import os
from rest_framework import viewsets, status
from Estabelecimento.models import Estabelecimento
from .serializers import EstabelecimentoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import requests
from dotenv import load_dotenv
load_dotenv()

class EstabelecimentoViewSet(viewsets.ModelViewSet):
    queryset = Estabelecimento.objects.all()
    serializer_class = EstabelecimentoSerializer
    
    def validate_cep(self, cep):
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200 and not response.json().get('erro'):
            return True
        return False

    def validate_email(self, email):
        api_key=os.getenv('EMAIL_API_KEY')
        response = requests.get(f'https://emailverification.whoisxmlapi.com/api/v3?apiKey={api_key}&emailAddress={email}')
        if response.status_code == 200:
            result = response.json()
            return result.get('smtpCheck') == 'true'
        return False

    def validate_contact(self, contato):
        if len(contato) in [10, 11] and contato.isdigit():
            return True
        return False

    def create(self, request, *args, **kwargs):
        data = request.data
        if not all(data.values()):
            return Response({"error": "Todos os campos devem ser preenchidos."}, status=status.HTTP_400_BAD_REQUEST)

        if Estabelecimento.objects.filter(nome=data['nome']).exists():
            return Response({"error": "Este estabelecimento já está cadastrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'usuario' in data and 'username' in data['usuario']:
            if User.objects.filter(username=data['usuario']['username']).exists():
                return Response({"error": "Este nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)


        if not self.validate_cep(data['cep']):
            return Response({"error": "CEP inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if not self.validate_contact(data['contato']):
            return Response({"error": "Contato inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if not self.validate_email(data['email']):
            return Response({"error": "E-mail inválido."}, status=status.HTTP_400_BAD_REQUEST)

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
