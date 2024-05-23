from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from Agendamentos.models import AgendamentosPeloEstabelecimento, AgendamentosPeloCliente
from .serializers import AgendamentosClientesSerializer, AgendamentosEstabelecimentoSerializer
from Clientes.models import Clientes
from Estabelecimento.models import Estabelecimento
from django.shortcuts import get_object_or_404
from datetime import date, timedelta, datetime
from django.db.models import F

class AgendamentoClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgendamentosPeloCliente.objects.all()
    serializer_class = AgendamentosClientesSerializer
    
    def list(self, request):
        cliente_id = request.query_params.get('cliente_id')
        if not cliente_id:
            return Response({'error': 'O ID do cliente é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        cliente = get_object_or_404(Clientes, id=cliente_id)
        quetyset = AgendamentosPeloCliente.objects.filter(cliente=cliente)
        serializer = AgendamentosClientesSerializer(quetyset, many=True)
        return Response(serializer.data)
    
    def validated_agendamentoCliente(self, data):
        estabelecimento = data.get('estabelecimento')
        cliente = data.get('cliente')
        servico = data.get('servico')
        horario_selecionado = data.get('horario_selecionado')
        dia_selecionado = data.get('dia_selecionado')
        
        if AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento, cliente=cliente, servico=servico, horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado).exists():
            raise ValidationError('Você já realizou este mesmo agendamento.')
        
        elif AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento,horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado).exists():
            raise ValidationError('Este horário já foi reservado.')
        
        elif AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento, servico=servico, dia_selecionado=dia_selecionado, cliente=cliente).exists():
            raise ValidationError('Você já reservou este serviço no mesmo dia em outro horário.')
        
        elif AgendamentosPeloCliente.objects.filter(horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado, cliente=cliente).exists():
            raise ValidationError('Você já reservou este horário em outro estabelecimento.')
        
    def delete_expired_agendamentos(self):
        agora = datetime.now()
        agendamentos_expirados = AgendamentosPeloCliente.objects.filter(
            horario_selecionado__lt = agora - timedelta(minutes=5)
        )
        agendamentos_expirados.delete()
        
    def create(self, request, *args, **kwargs):
        self.delete_expired_agendamentos()
        self.validated_agendamentoCliente(request.data)
        return super().create(request, *args, **kwargs)
    
    
    
class AgendamentoEstabelecimentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgendamentosPeloEstabelecimento.objects.all()
    serializer_class = AgendamentosEstabelecimentoSerializer
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return Response({'error': 'O ID do estabelecimento é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        estabelecimento = get_object_or_404(Estabelecimento, id=estabelecimento_id)

        agendamentos_cliente = AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento)
        agendamentos_estabelecimento = AgendamentosPeloEstabelecimento.objects.filter(estabelecimento=estabelecimento)

        agendamentos_cliente_serializer = AgendamentosClientesSerializer(agendamentos_cliente, many=True)
        agendamentos_estabelecimento_serializer = AgendamentosEstabelecimentoSerializer(agendamentos_estabelecimento, many=True)

        combined_data = agendamentos_cliente_serializer.data + agendamentos_estabelecimento_serializer.data

        return Response(combined_data)
    
    def validated_agendamentoEstabelecimento(self, data):
        estabelecimento = data.get('estabelecimento')
        nome = data.get('nome')
        contato = data.get('contato')
        servico = data.get('servico')
        horario_selecionado = data.get('horario_selecionado')
        dia_selecionado = data.get('dia_selecionado')
        
        if AgendamentosPeloEstabelecimento.objects.filter(estabelecimento=estabelecimento, nome=nome, contato=contato, servico=servico, horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado).exists():
            raise ValidationError('Você já realizou este mesmo agendamento.')
        
        elif AgendamentosPeloEstabelecimento.objects.filter(estabelecimento=estabelecimento,horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado).exists():
            raise ValidationError('Este horário já foi reservado.')
        
        elif AgendamentosPeloEstabelecimento.objects.filter(horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado, nome=nome, contato=contato).exists():
            raise ValidationError('Esta pessoa já reservou este horário em outro estabelecimento.')
        
        elif AgendamentosPeloEstabelecimento.objects.filter(dia_selecionado=dia_selecionado, nome=nome, contato=contato, estabelecimento=estabelecimento, servico=servico).exists():
            raise ValidationError('Esta pessoa já reservou este serviço no mesmo dia em outro horário.')
        
    def delete_expired_agendamentos(self):
        agora = datetime.now()
        agendamentos_expirados = AgendamentosPeloEstabelecimento.objects.filter(
            horario_selecionado__lt=agora - timedelta(minutes=5)
        )
        agendamentos_expirados.delete()

    def create(self, request, *args, **kwargs):
        self.delete_expired_agendamentos() 
        self.validated_agendamentoEstabelecimento(request.data)
        return super().create(request, *args, **kwargs)
    

class AgendamentosHojeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return Response({'error': 'O ID do estabelecimento é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        estabelecimento = get_object_or_404(Estabelecimento, id=estabelecimento_id)

        hoje = date.today()
        agendamentos_cliente = AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento, dia_selecionado=hoje)
        agendamentos_estabelecimento = AgendamentosPeloEstabelecimento.objects.filter(estabelecimento=estabelecimento, dia_selecionado=hoje)

        agendamentos_cliente_serializer = AgendamentosClientesSerializer(agendamentos_cliente, many=True)
        agendamentos_estabelecimento_serializer = AgendamentosEstabelecimentoSerializer(agendamentos_estabelecimento, many=True)

        combined_data = agendamentos_cliente_serializer.data + agendamentos_estabelecimento_serializer.data

        return Response(combined_data)

class AgendamentosSemanaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return Response({'error': 'O ID do estabelecimento é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        estabelecimento = get_object_or_404(Estabelecimento, id=estabelecimento_id)

        hoje = date.today()
        inicio_semana = hoje - timedelta(days=hoje.weekday() + 1 if hoje.weekday() != 6 else 0)
        fim_semana = inicio_semana + timedelta(days=6)

        agendamentos_cliente = AgendamentosPeloCliente.objects.filter(
            estabelecimento=estabelecimento,
            dia_selecionado__range=[inicio_semana, fim_semana]
        )
        agendamentos_estabelecimento = AgendamentosPeloEstabelecimento.objects.filter(
            estabelecimento=estabelecimento,
            dia_selecionado__range=[inicio_semana, fim_semana]
        )

        agendamentos_cliente_serializer = AgendamentosClientesSerializer(agendamentos_cliente, many=True)
        agendamentos_estabelecimento_serializer = AgendamentosEstabelecimentoSerializer(agendamentos_estabelecimento, many=True)

        combined_data = agendamentos_cliente_serializer.data + agendamentos_estabelecimento_serializer.data

        return Response(combined_data)