from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Agendamentos.models import AgendamentosPeloEstabelecimento, AgendamentosPeloCliente
from .serializers import AgendamentosClientesSerializer, AgendamentosEstabelecimentoSerializer
from Clientes.models import Clientes
from Estabelecimento.models import Estabelecimento
from django.shortcuts import get_object_or_404
from datetime import date, timedelta, datetime
from django.db.models import F
from AgendAR.utils import send_error_response

class AgendamentoClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgendamentosPeloCliente.objects.all()
    serializer_class = AgendamentosClientesSerializer
    
    def list(self, request):
        cliente_id = request.query_params.get('cliente_id')
        if not cliente_id:
            return send_error_response( 'O ID do cliente é obrigatório.')
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
            return send_error_response('Você já realizou este mesmo agendamento.')
        
        elif AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento,horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado).exists():
            return send_error_response('Este horário já foi reservado.')
        
        elif AgendamentosPeloCliente.objects.filter(estabelecimento=estabelecimento, servico=servico, dia_selecionado=dia_selecionado, cliente=cliente).exists():
            return send_error_response('Você já reservou este serviço no mesmo dia em outro horário.')
        
        elif AgendamentosPeloCliente.objects.filter(horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado, cliente=cliente).exists():
            return send_error_response('Você já reservou este horário em outro estabelecimento.')
            
    def create(self, request, *args, **kwargs):
        self.validated_agendamentoCliente(request.data)
        return super().create(request, *args, **kwargs)
    
    
    
class AgendamentoEstabelecimentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgendamentosPeloEstabelecimento.objects.all()
    serializer_class = AgendamentosEstabelecimentoSerializer
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return send_error_response("O ID do estabelecimento é obrigatório.")
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
            return send_error_response('Você já realizou este mesmo agendamento.')
        
        elif AgendamentosPeloEstabelecimento.objects.filter(estabelecimento=estabelecimento,horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado).exists():
            return send_error_response('Este horário já foi reservado.')
        
        elif AgendamentosPeloEstabelecimento.objects.filter(horario_selecionado=horario_selecionado, dia_selecionado=dia_selecionado, nome=nome, contato=contato).exists():
            return send_error_response('Esta pessoa já reservou este horário em outro estabelecimento.')
        
        elif AgendamentosPeloEstabelecimento.objects.filter(dia_selecionado=dia_selecionado, nome=nome, contato=contato, estabelecimento=estabelecimento, servico=servico).exists():
            return send_error_response('Esta pessoa já reservou este serviço no mesmo dia em outro horário.')
        

    def create(self, request, *args, **kwargs):
        self.validated_agendamentoEstabelecimento(request.data)
        return super().create(request, *args, **kwargs)
    

class AgendamentosHojeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return send_error_response('O ID do estabelecimento é obrigatório.')
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
            return send_error_response('O ID do estabelecimento é obrigatório.')
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
    
class AgendamentosStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return send_error_response('O ID do estabelecimento é obrigatório.')

        estabelecimento = Estabelecimento.objects.filter(id=estabelecimento_id).first()
        if not estabelecimento:
            return send_error_response('Estabelecimento não encontrado.')

        hoje = date.today()
        inicio_mes = hoje.replace(day=1)
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        def contar_agendamentos(queryset, inicio, fim=None):
            filtro = {'estabelecimento': estabelecimento, 'dia_selecionado__gte': inicio}
            if fim:
                filtro['dia_selecionado__lte'] = fim
            return queryset.filter(**filtro).count()

        agendamentos_mensais = contar_agendamentos(
            AgendamentosPeloCliente.objects, inicio_mes
        ) + contar_agendamentos(
            AgendamentosPeloEstabelecimento.objects, inicio_mes
        )

        agendamentos_semanais = contar_agendamentos(
            AgendamentosPeloCliente.objects, inicio_semana, fim_semana
        ) + contar_agendamentos(
            AgendamentosPeloEstabelecimento.objects, inicio_semana, fim_semana
        )

        agendamentos_diarios = contar_agendamentos(
            AgendamentosPeloCliente.objects, hoje, hoje
        ) + contar_agendamentos(
            AgendamentosPeloEstabelecimento.objects, hoje, hoje
        )

        def calcular_percentual(atual, passado):
            return ((atual - passado) / passado) * 100 if passado else 0

        # Calculando agendamentos passados
        mes_passado = inicio_mes - timedelta(days=1)
        inicio_mes_passado = mes_passado.replace(day=1)
        fim_mes_passado = mes_passado

        agendamentos_mensais_passado = contar_agendamentos(
            AgendamentosPeloCliente.objects, inicio_mes_passado, fim_mes_passado
        ) + contar_agendamentos(
            AgendamentosPeloEstabelecimento.objects, inicio_mes_passado, fim_mes_passado
        )

        inicio_semana_passada = inicio_semana - timedelta(days=7)
        fim_semana_passada = fim_semana - timedelta(days=7)

        agendamentos_semanais_passado = contar_agendamentos(
            AgendamentosPeloCliente.objects, inicio_semana_passada, fim_semana_passada
        ) + contar_agendamentos(
            AgendamentosPeloEstabelecimento.objects, inicio_semana_passada, fim_semana_passada
        )

        dia_passado = hoje - timedelta(days=1)

        agendamentos_diarios_passado = contar_agendamentos(
            AgendamentosPeloCliente.objects, dia_passado, dia_passado
        ) + contar_agendamentos(
            AgendamentosPeloEstabelecimento.objects, dia_passado, dia_passado
        )

        response_data = {
            'agendamentos_mensais': agendamentos_mensais,
            'agendamentos_semanais': agendamentos_semanais,
            'agendamentos_diarios': agendamentos_diarios,
            'percentual_mensal': calcular_percentual(agendamentos_mensais, agendamentos_mensais_passado),
            'percentual_semanal': calcular_percentual(agendamentos_semanais, agendamentos_semanais_passado),
            'percentual_diario': calcular_percentual(agendamentos_diarios, agendamentos_diarios_passado),
        }

        return Response(response_data)
