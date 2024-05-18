import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Localizacao.api.serializers import LocalizacaoSerializer

class LocalicacaoToEnderecoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LocalizacaoSerializer(data=request.data)
        if serializer.is_valid():
            localicacao = serializer.save()
            estabelecimento = localicacao.estabelecimento
            
            response = requests.get(
                f'https://maps.googleapis.com/maps/api/geocode/json?latlng={localicacao.lat},{localicacao.lng}&key=AIzaSyB_77CX7GW1gdmCdzXYWB8uUJnWN6blRRE'
            )
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    endereco = data['results'][0]['address_components']
                    for component in endereco:
                        if 'street_number' in component['types']:
                            estabelecimento.numeroEndereco = component['long_name']
                        elif 'route' in component['types']:
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
                    return Response({'error': 'Não foi possível encontrar um endereço para estas coordenadas'}, status=400)
            else:
                return Response({'error': 'Erro ao consultar a API do Google'}, status=response.status_code)
        return Response(serializer.errors, status=400)
