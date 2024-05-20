from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HorarioViewSet, TempoHorarioViewSet

router = DefaultRouter()
router.register('', HorarioViewSet)
router.register(r'tempo_horarios', TempoHorarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
