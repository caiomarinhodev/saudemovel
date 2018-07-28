from django.contrib import admin

from app.models import *

"""
admin.py: Definicao de classes para gerenciar no sistema de admin do Django.
"""
__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"


class PacienteInline(admin.TabularInline):
    model = Paciente


class AtestadoInline(admin.TabularInline):
    model = Atestado


class ProntuarioInline(admin.TabularInline):
    model = Prontuario


class ConsultaInline(admin.TabularInline):
    model = Consulta


class PacienteAdmin(admin.ModelAdmin):
    inlines = [ConsultaInline, AtestadoInline]
    search_fields = (
        'user__first_name',
    )
    list_display = (
        'id', 'user', 'nome', 'sobrenome', 'cpf', 'foto', 'endereco', 'numero', 'data_nascimento', 'created_at')

    def nome(self, obj):
        return obj.user.first_name

    def sobrenome(self, obj):
        return obj.user.last_name


class ConsultaAdmin(admin.ModelAdmin):
    search_fields = (
        'paciente__user__first_name',
    )
    list_display = ('paciente_nome', 'especialista', 'data', 'local', 'cidade', 'id', 'created_at')

    def paciente_nome(self, obj):
        return obj.paciente.user.first_name

    def especialista_nome(self, obj):
        return obj.especialista.user.first_name


class AtestadoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'paciente', 'especialista', 'data', 'created_at')


class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'especialista', 'data', 'cid', 'local', 'created_at',)


class AtendenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'foto', 'horario', 'created_at',)


class EspecialistaAdmin(admin.ModelAdmin):
    inlines = [ConsultaInline, AtestadoInline, ProntuarioInline]
    search_fields = (
        'user__first_name',
    )
    list_display = ('id', 'user', 'crm', 'foto', 'created_at')


admin.site.register(Especialista, EspecialistaAdmin)
admin.site.register(Atendente, AtendenteAdmin)
admin.site.register(Prontuario, ProntuarioAdmin)
admin.site.register(Atestado, AtestadoAdmin)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Paciente, PacienteAdmin)
