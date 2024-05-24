from rest_framework import serializers
from Agendamentos.models import AgendamentosPeloCliente, AgendamentosPeloEstabelecimento
from Servicos.models import Servicos
from Clientes.models import Clientes
class ServicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos
        fields = ('id', 'nome')

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = ('id', 'nome', 'contato')

class AgendamentosClientesSerializer(serializers.ModelSerializer):
    servico = ServicosSerializer()
    cliente = ClientesSerializer()
    class Meta:
        model = AgendamentosPeloCliente
        fields = ('id', 'estabelecimento', 'servico', 'cliente', 'horario_selecionado', 'dia_selecionado', 'horario')

class AgendamentosEstabelecimentoSerializer(serializers.ModelSerializer):
    servico = serializers.PrimaryKeyRelatedField(queryset=Servicos.objects.all())
    servico_nome = serializers.SerializerMethodField()
    class Meta:
        model = AgendamentosPeloEstabelecimento
        fields = ('id', 'estabelecimento', 'servico', 'servico_nome', 'nome', 'contato', 'horario_selecionado', 'dia_selecionado', 'horario')
    
    def get_servico_nome(self, obj):
        return obj.servico.nome if obj.servico else None