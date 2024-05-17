from django.contrib import admin
from .models import Localicazao

@admin.register(Localicazao)
class LocalicazaoAdmin(admin.ModelAdmin):
    list_display = ['lat', 'lng', 'estabelecimento']
    search_fields = ['estabelecimento__nome']
