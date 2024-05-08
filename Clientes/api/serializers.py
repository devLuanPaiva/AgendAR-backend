from rest_framework import serializers
from django.contrib.auth.models import User
from Clientes.models import Clientes

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
class ClientesSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Clientes
        fields = ('id', 'nome', 'email', 'contato', 'usuario')
    
    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        user = User.objects.create_user(**user_data)
        clientes = Clientes.objects.create(usuario=user, **validated_data)
        return clientes
        