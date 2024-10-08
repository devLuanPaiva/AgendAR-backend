from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from Horarios.models import Horario, TempoHorario
from .serializers import HorarioSerializer, TempoHorarioSerializer
from Estabelecimento.models import Estabelecimento
from django.shortcuts import get_object_or_404
from AgendAR.utils import send_error_response

class HorarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return send_error_response('O ID do estabelecimento é obrigatório.')
        estabelecimento = get_object_or_404(Estabelecimento, id=estabelecimento_id)
        queryset = Horario.objects.filter(estabelecimento=estabelecimento)
        serializer = HorarioSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        self.validate_horario(request.data)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        self.validate_horario(request.data)
        return super().update(request, *args, **kwargs)
   
    
    def validate_horario(self, data):
        dia_da_semana = data.get('dia_da_semana')
        turno = data.get('turno')
        horario_inicio = data.get('horario_inicio')
        horario_fim = data.get('horario_fim')
        estabelecimento = data.get('estabelecimento')
        
        if Horario.objects.filter(dia_da_semana=dia_da_semana, turno=turno, horario_inicio=horario_inicio, horario_fim=horario_fim, estabelecimento=estabelecimento).exists():
            raise ValidationError('Este horário já está cadastrado para o estabelecimento.')
        if Horario.objects.filter(dia_da_semana=dia_da_semana, turno=turno, estabelecimento=estabelecimento).exists():
            raise ValidationError('Já existe um horário cadastrado para este turno, neste dia e neste estabelecimento.')
        
        if turno == "NOITE":
            horario_inicio_hours, _ = map(int, horario_inicio.split(':'))
            horario_fim_hours, _ = map(int, horario_fim.split(':'))

            if (horario_inicio_hours or horario_fim_hours) < 18:
                raise ValidationError('Horário inicial para o turno da noite deve ser 18h ou posterior.')
        
        elif turno == "TARDE":
            horario_inicio_hours, _ = map(int, horario_inicio.split(':'))
            horario_fim_hours, _ = map(int, horario_fim.split(':'))
            if not (12 <= horario_inicio_hours <= 18) or not (12 <= horario_fim_hours <= 18):
                raise ValidationError('O horário para o turno da tarde deve estar entre 12h e 18h.')
            
        elif turno == "MANHA":
            horario_inicio_hours, _ = map(int, horario_inicio.split(':'))
            horario_fim_hours, _ = map(int, horario_fim.split(':'))
            if (horario_inicio_hours  or horario_fim_hours) > 12:
                raise ValidationError('Horário para o turno da manhã deve ser inferior à 12h.')
            
        

        horario_inicio_hours, horario_inicio_minutes = map(int, horario_inicio.split(':'))
        horario_fim_hours, horario_fim_minutes = map(int, horario_fim.split(':'))
        
        if horario_inicio_hours > horario_fim_hours or (horario_inicio_hours == horario_fim_hours and horario_inicio_minutes >= horario_fim_minutes):
            raise ValidationError('Horário escolhido é inválido. O horário de início não pode ser maior ou igual ao de término.')

    
    
class TempoHorarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TempoHorario.objects.all()
    serializer_class = TempoHorarioSerializer
    
    def list(self, request):
        estabelecimento_id = request.query_params.get('estabelecimento_id')
        if not estabelecimento_id:
            return send_error_response('O ID do estabelecimento é obrigatório.')
        estabelecimento = get_object_or_404(Estabelecimento, id=estabelecimento_id)
        quetyset = TempoHorario.objects.filter(estabelecimento=estabelecimento)
        serializer = TempoHorarioSerializer(quetyset, many=True)
        return Response(serializer.data)
