import os
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Localizacao.api.serializers import LocalizacaoSerializer
from rest_framework.exceptions import ValidationError
from dotenv import load_dotenv

load_dotenv()

class LocalicacaoToEnderecoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LocalizacaoSerializer(data=request.data)
        if serializer.is_valid():
            localicacao = serializer.save()
            estabelecimento = localicacao.estabelecimento
            api_key = os.getenv('GOOGLE_MAPS_API_KEY')
            response = requests.get(
                f'https://maps.googleapis.com/maps/api/geocode/json?latlng={localicacao.lat},{localicacao.lng}&key={api_key}'
            )
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    endereco = data['results'][0]['address_components']
                    for component in endereco:
                        if 'route' in component['types']:
                            estabelecimento.rua = component['long_name']
                        elif 'sublocality_level_1' in component['types']:
                            estabelecimento.bairro = component['long_name']
                        elif 'administrative_area_level_2' in component['types']:
                            estabelecimento.cidade = component['long_name']
                        elif 'administrative_area_level_1' in component['types']:
                            estabelecimento.estado = component['short_name']
                        elif 'postal_code' in component['types']:
                            estabelecimento.cep = component['long_name']
                    estabelecimento.save()
                    return Response({'message': 'Endereço atualizado com sucesso'}, status=200)
                else:
                    return ValidationError('Não foi possível encontrar um endereço para estas coordenadas')
            else:
                return ValidationError('Erro ao consultar a API do Google')
        return Response(serializer.errors, status=400)
