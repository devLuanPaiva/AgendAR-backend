from rest_framework import serializers
from Localizacao.models import Localicazao

class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localicazao
        fields = ('lat', 'lng', 'estabelecimento')