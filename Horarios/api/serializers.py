from rest_framework import serializers
from Horarios.models import Horario, TempoHorario
class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class TempoHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempoHorario
        fields = ['tempo', 'id']