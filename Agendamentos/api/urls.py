from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgendamentoClienteViewSet, AgendamentoEstabelecimentoViewSet, AgendamentosHojeViewSet, AgendamentosSemanaViewSet, AgendamentosStatsViewSet

router = DefaultRouter()
router.register(r'clientes', AgendamentoClienteViewSet, basename='agendamentos-clientes')
router.register(r'estabelecimentos', AgendamentoEstabelecimentoViewSet, basename='agendamentos-estabelecimentos')
router.register(r'hoje', AgendamentosHojeViewSet, basename='hoje')
router.register(r'semana', AgendamentosSemanaViewSet, basename='semana')
router.register(r'dados-estatisticos', AgendamentosStatsViewSet, basename='dados-estatisticos')


urlpatterns = [
    path('', include(router.urls)),
]