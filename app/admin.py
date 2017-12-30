from django.contrib import admin

from app.models import *

"""
admin.py: Definicao de classes para gerenciar no painel de admin do Django.
"""
__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"


class PontoInline(admin.TabularInline):
    model = Ponto


class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cpf', 'phone', 'is_online', 'placa', 'is_approved', 'ocupado', 'photo')


class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'id', 'full_address', 'photo', 'is_online', 'created_at')


class PontoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'endereco', 'numero', 'bairro', 'created_at', 'status', 'duration', 'distance')


class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        PontoInline,
    ]
    list_display = ('estabelecimento',
                    'id', 'motorista', 'valor_total', 'status', 'is_complete', 'coletado', 'duration', 'distance',
                    'created_at')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'type_message', 'to', 'is_read')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'lat', 'lng', 'created_at')


class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'valor_madrugada', 'id')


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'nota', 'pedido')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('u_from', 'u_to', 'pedido', 'id', 'is_read', 'created_at')


admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Ponto, PontoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Bairro, BairroAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Message, MessageAdmin)
