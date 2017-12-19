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
    list_display = ('id', 'cliente', 'endereco', 'numero', 'bairro', 'created_at')


class PedidoAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'estabelecimento', 'motorista', 'valor_total', 'status', 'is_complete', 'coletado',
    'created_at')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'type_message', 'to', 'is_read')
    

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lat', 'lng', 'created_at')


admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Ponto, PontoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Location, LocationAdmin)