from rest_framework import serializers
from django.contrib.auth.models import User
from Estabelecimento.models import Estabelecimento

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
class EstabelecimentoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Estabelecimento
        fields = ('id', 'nome', 'cep', 'cidade', 'rua', 'estado', 'bairro', 'numeroEndereco', 'email', 'contato', 'usuario')

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        user = User.objects.create_user(**user_data)
        estabelecimento = Estabelecimento.objects.create(usuario=user, **validated_data)
        return estabelecimento    