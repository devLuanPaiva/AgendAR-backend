from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Estabelecimento.api.views import UserInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view()),
    path('estabelecimento/', include('Estabelecimento.api.urls')),
    path('servicos/', include('Servicos.api.urls')),
    path('clientes/', include('Clientes.api.urls')),
    path('horarios/', include('Horarios.api.urls')),
    path('localizacao/', include('Localizacao.api.urls')),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
]
