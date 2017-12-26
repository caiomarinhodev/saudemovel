from datetime import datetime

from django import template

from app.models import Motorista

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return float(float(value) / float(arg))
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def soma_avaliacao(value):
    try:
        sum = 0.0
        for c in value:
            sum = float(sum) + float(c.nota)
        return float(float(sum) / float(len(value)))
    except (ValueError, ZeroDivisionError):
        return "Nao Avaliado"


@register.filter
def corridas_mes(motorista):
    try:
        now = datetime.now()
        return motorista.user.pedido_set.filter(created_at__month=now.month)
    except (Motorista.DoesNotExist, Exception):
        return None


@register.filter
def corridas_hoje(motorista):
    try:
        now = datetime.now()
        return motorista.user.pedido_set.filter(created_at__day=now.day)
    except (Motorista.DoesNotExist, Exception):
        return None


@register.filter
def ganhos_mes(motorista):
    try:
        now = datetime.now()
        corridas_mes = motorista.user.pedido_set.filter(created_at__month=now.month)
        ganho_mes = 0.0
        for pedido in corridas_mes:
            ganho_mes = float(ganho_mes) + float(pedido.valor_total)
        return ganho_mes
    except (Motorista.DoesNotExist, Exception):
        return 0.0


@register.filter
def ganhos_hoje(motorista):
    try:
        now = datetime.now()
        corridas_hoje = motorista.user.pedido_set.filter(created_at__day=now.day)
        ganho_hoje = 0.0
        for pedido in corridas_hoje:
            ganho_hoje = float(ganho_hoje) + float(pedido.valor_total)
        return ganho_hoje
    except (Motorista.DoesNotExist, Exception):
        return 0.0
