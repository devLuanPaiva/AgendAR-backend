from rest_framework import serializers
from Servicos.models import Servicos

class ServicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos
        fields = ('nome', 'valor', 'descricao', 'estabelecimento', 'id')