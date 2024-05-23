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
        fields = ('id', 'nome', 'cep', 'cidade', 'rua', 'estado', 'bairro', 'email', 'contato', 'usuario')

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        user = User.objects.create_user(**user_data)
        estabelecimento = Estabelecimento.objects.create(usuario=user, **validated_data)
        return estabelecimento
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('usuario')
        user = instance.usuario
        
        instance.nome = validated_data.get('nome', instance.nome)
        instance.cep = validated_data.get('cep', instance.cep)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.cidade = validated_data.get('cidade', instance.cidade)
        instance.rua = validated_data.get('rua', instance.rua)
        instance.bairro = validated_data.get('bairro', instance.bairro)
        instance.email = validated_data.get('email', instance.email)
        instance.contato = validated_data.get('contato', instance.contato)
        instance.save()
        
        user.username = user_data.get('username', user.username)
        if 'password' in user_data:
            user.set_password(user_data['password'])
        user.save()
        
        return instance  