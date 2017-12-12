from django.contrib import admin

from app.models import *

"""
admin.py: Definicao de classes para gerenciar no painel de admin do Django.
"""
__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"


class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')


class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')


class PercursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class PontoAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class PedidoAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'nome_cliente', 'estabelecimento', 'motorista', 'valor_total', 'status', 'is_complete', 'coletado',
    'created_at')


admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Ponto, PontoAdmin)
admin.site.register(Pedido, PedidoAdmin)
