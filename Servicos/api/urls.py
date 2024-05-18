from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicosViewSet

router = DefaultRouter()
router.register('', ServicosViewSet, basename='servicos')

urlpatterns = [
    path('', include(router.urls)),
]
