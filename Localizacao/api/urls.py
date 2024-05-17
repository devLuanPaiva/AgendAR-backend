from django.urls import path
from .views import LocalicacaoToEnderecoView

urlpatterns = [
    path('coordenadas/', LocalicacaoToEnderecoView.as_view() ,name='coordenadas-to-endereco')
]
