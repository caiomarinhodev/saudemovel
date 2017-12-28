from datetime import datetime

from django import template

from app.models import Motorista
from app.views.geocoding import calculate_matrix_distance

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
def get_latitude(motorista):
    try:
        return motorista.user.location_set.all().order_by('-created_at').last().lat
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0


@register.filter
def get_longitude(motorista):
    try:
        return motorista.user.location_set.all().order_by('-created_at').last().lng
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0


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


@register.filter
def calculate_distance(pedido):
    try:
        ptoi = pedido.ponto_set.first()
        distance = 0
        duration = 0
        for pto in pedido.ponto_set.all():
            origin = str(ptoi.lat) + "," + str(ptoi.lng)
            destin = str(pto.lat) + "," + str(pto.lng)
            calc = calculate_matrix_distance(origin, destin)
            distance = distance + int(calc['dis_value'])
            duration = duration + int(calc['dur_value'])
            ptoi = pto
        destin = str(pedido.estabelecimento.lat) + "," + str(pedido.estabelecimento.lng)
        distance = distance + int(calculate_matrix_distance(pto, destin)['dis_value'])
        duration = duration + int(calculate_matrix_distance(pto, destin)['dur_value'])
        pedido.duration = duration
        pedido.distance = distance
        pedido.save()
        return float(distance / 1000.0)
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0
