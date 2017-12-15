#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from app.mixins.CustomContextMixin import RedirectMotoristaOcupadoView


from app.forms import PontoFormSet
from app.models import Pedido, Estabelecimento, Motorista, Notification
from app.views.snippet_template import render_block_to_string


class OrderMotoristaDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/order_view.html'
    context_object_name = 'pedido'


class RouteMotoristaDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/route_view.html'
    context_object_name = 'pedido'


class MapRouteMotoristaView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/map_view.html'
    context_object_name = 'pedido'


class PedidosLojaListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos/list_pedidos_loja.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user).order_by('-created_at')


class PedidosMotoristaListView(LoginRequiredMixin, RedirectMotoristaOcupadoView, ListView):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos/list_pedidos_motorista.html'

    def get_queryset(self):
        return Pedido.objects.filter(is_complete=False, coletado=False, status=True).order_by('-created_at')


class EntregasMotoristaListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'entregas/list_entregas_motorista.html'

    def get_queryset(self):
        return Pedido.objects.filter(motorista=self.request.user).order_by('-published_at')


class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    success_url = '/app/pedidos/loja/'
    fields = ['estabelecimento',]
    template_name = 'pedidos/add_pedido.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }

    def get_context_data(self, **kwargs):
        data = super(PedidoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pontoset'] = PontoFormSet(self.request.POST)
        else:
            data['pontoset'] = PontoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pontoset = context['pontoset']
        with transaction.atomic():
            self.object = form.save()
            if pontoset.is_valid():
                pontoset.instance = self.object
                pontoset.save()
        message = "Um novo pedido foi feito pela " + self.request.user.first_name
        for m in Motorista.objects.all():
            if m.is_online and not m.ocupado:
                n = Notification(type_message='NOVO_PEDIDO', to=m.user, message=message)
                n.save()
        return super(PedidoCreateView, self).form_valid(form)


def delete_pedido(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário precisa estar logado para esta operação")
        raise PermissionDenied("Usuário precisa estar logado para esta operação")
    else:
        pedido = Pedido.objects.get(id=pk)
        try:
            user_motorista = pedido.motorista
            motorista = Motorista.objects.get(user=user_motorista)
        except:
            user_motorista = None
        if user_motorista:
            if user_motorista.pedido_set.last() == pedido:
                motorista.ocupado = False
                motorista.save()
                loja = Estabelecimento.objects.get(user=request.user)
                if motorista.is_online:
                    message = "O Pedido que voce ia entregar foi cancelado pela loja " + request.user.first_name + ". Desculpe pelo transtorno! Qualquer coisa, ligue para a loja: " + loja.phone
                    n = Notification(type_message='DELETE_LOJA', to=motorista.user, message=message)
                    n.save()
        pedido.delete()
        messages.success(request, "Pedido deletado com sucesso")
        return HttpResponseRedirect('/app/pedidos/loja/')


@require_http_methods(["GET"])
def get_pedidos_motorista(request):
    pedidos = Pedido.objects.filter(is_complete=False, coletado=False, status=True).order_by('-created_at')
    context = Context({'pedidos': pedidos, 'user': request.user})
    return_str = render_block_to_string('includes/table_pedidos_motorista.html', context)
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def get_entregas_motorista(request):
    pedidos = Pedido.objects.filter(motorista=request.user).order_by('-published_at')
    context = Context({'pedidos': pedidos, 'user': request.user})
    return_str = render_block_to_string('includes/table_entregas_motorista.html', context)
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def accept_corrida(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    if pedido.motorista:
        messages.error(request, 'Outro Motorista pegou esta entrega antes de você')
        return HttpResponseRedirect('/app/pedidos/motorista/')
    else:
        pedido.status = False
        pedido.motorista = request.user
        pedido.save()
        motorista = Motorista.objects.get(user=request.user)
        motorista.ocupado = True
        motorista.save()
        if pedido.estabelecimento.is_online:
            message = "Um motorista aceitou fazer a entrega do Pedido ID #" + str(
                pedido.pk) + ". Qualquer problema, ligue para o motorista: " + motorista.phone
            n = Notification(type_message='ACCEPT_ORDER', to=pedido.estabelecimento.user, message=message)
            n.save()
        return redirect('/app/entregas/motorista')


#@require_http_methods(["GET"])
#def cancel_corrida_motorista(request, pk_pedido):
#    pedido = Pedido.objects.get(id=pk_pedido)
#    pedido.status = True
#    pedido.motorista = None
#    pedido.is_complete = False
#    pedido.coletado = False
#    pedido.save()
#    motorista = Motorista.objects.get(user=request.user)
#    motorista.ocupado = False
#    motorista.save()
#    message = "O motorista " + motorista.user.first_name + " cancelou a entrega do Pedido ID #" + str(
#        pedido.pk) + ". Qualquer problema, ligue para o motorista: " + motorista.phone
#    n = Notification(type_message='CANCEL_ORDER', to=pedido.estabelecimento.user, message=message)
#    n.save()
#    return redirect('/app/pedidos/motorista')


@require_http_methods(["GET"])
def liberar_corrida(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    pedido.coletado = True
    pedido.save()
    if Motorista.objects.get(user=pedido.motorista).is_online:
        message = "Voce foi liberado pela loja para realizar a(s) entrega(s). Sua Rota atual estara no menu ENTREGAS. Qualquer problema, ligue para a loja: " + pedido.estabelecimento.phone
        n = Notification(type_message='ENABLE_ROTA', to=pedido.motorista, message=message)
        n.save()
    return redirect('/app/acompanhar')

# TODO: Motorista ao logar ou ao sair da page qualquer e estiver OCUPADO(entregando), notificar o endereco da entrega e redirecionar para /entregas
# TODO: Implementar botao em acompanhamentos da loja para acompanhar entrega, apos liberado.
# TODO: Implementar notificacao p/ motorista de que o produto foi liberado para entrega, e mostrar rota(mapa).
# TODO: Notificar Loja de que motorista X saiu para entrega e pode ser acompanhado em acompanhamentos id #.
# TODO: Implementar botao de Finalizar Entrega em entregas do motorista, para finalizar uma entrega.
# TODO: Implementar notificacao p/ loja de que o produto foi entregue.
# TODO: Definir Times de acordo com prioridades e testes.
# TODO: Refatorar codigo duplicado
# TODO: Remover codigo comentado
# TODO: Organizar as pastas de templates
# TODO: Fechar Release e Deploy