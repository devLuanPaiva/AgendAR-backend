from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view()),
    path('estabelecimento/', include('Estabelecimento.api.urls')),
    path('clientes/', include('Clientes.api.urls')),
    path('token/refresh/', TokenRefreshView.as_view()),
]
