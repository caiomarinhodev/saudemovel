#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.http import require_http_methods

from app.models import Notification
from app.views.snippet_template import render_block_to_string


@require_http_methods(["GET"])
def notificar_novo_pedido_motorista(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='NOVO_PEDIDO', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_delete_loja_motorista(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='DELETE_LOJA', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_accept_order_loja(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='ACCEPT_ORDER', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_cancel_order_loja(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='CANCEL_ORDER', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_enable_rota_motorista(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='CANCEL_ORDER', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)
