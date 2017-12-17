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
from app.mixins.CustomContextMixin import RedirectMotoristaOcupadoView, CustomContextMixin
from django.shortcuts import render_to_response


from app.forms import PontoFormSet
from app.models import Pedido, Estabelecimento, Motorista, Notification, Ponto
from app.views.snippet_template import render_block_to_string


class OrderMotoristaDetailView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'pedidos/order_view.html'
    context_object_name = 'pedido'
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super(OrderMotoristaDetailView, self).get(request, *args, **kwargs)
        except:
            messages.error(request, 'Este pedido foi cancelado pela loja')
            return HttpResponseRedirect('/app/pedidos/motorista/')


class RouteMotoristaDetailView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'pedidos/route_view.html'
    context_object_name = 'pedido'
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super(RouteMotoristaDetailView, self).get(request, *args, **kwargs)
        except:
            messages.error(request, 'Este pedido foi cancelado pela loja')
            return HttpResponseRedirect('/app/pedidos/motorista/')


class MapRouteMotoristaView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'pedidos/map_view.html'
    context_object_name = 'pedido'
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super(MapRouteMotoristaView, self).get(request, *args, **kwargs)
        except:
            messages.error(request, 'Este pedido foi cancelado pela loja')
            return HttpResponseRedirect('/app/pedidos/motorista/')


class PedidosLojaListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos/list_pedidos_loja.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user).order_by('-created_at')


class PedidosMotoristaListView(LoginRequiredMixin, RedirectMotoristaOcupadoView, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos/list_pedidos_motorista.html'

    def get_queryset(self):
        return Pedido.objects.filter(is_complete=False, coletado=False, status=True).order_by('-created_at')


class EntregasMotoristaListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'entregas/list_entregas_motorista.html'

    def get_queryset(self):
        return Pedido.objects.filter(motorista=self.request.user).order_by('-published_at')


class PedidoCreateView(LoginRequiredMixin, CreateView, CustomContextMixin):
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
        print('>>>>>>>> Novo Pedido criado pela loja '+ self.request.user.first_name)
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
                    print('>>>>>>>> Motorista '+motorista.user.first_name+' teve seu pedido cancelado pela loja '+pedido.estabelecimento.user.first_name)
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
    try:
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
                print('>>>>>>>> Motorista '+motorista.user.first_name+' aceitou fazer a corrida para a loja '+pedido.estabelecimento.user.first_name)
                message = "Um motorista aceitou fazer a entrega do Pedido ID #" + str(
                    pedido.pk) + ". Qualquer problema, ligue para o motorista: " + motorista.phone
                n = Notification(type_message='ACCEPT_ORDER', to=pedido.estabelecimento.user, message=message)
                n.save()
                message = 'A Loja '+pedido.estabelecimento.user.first_name+', localizado na '+pedido.estabelecimento.full_address+', está aguardando a coleta.'
                no = Notification(type_message='DELETE_LOJA', to=pedido.motorista, message=message) # está delete loja por enquanto.
                no.save()
            return HttpResponseRedirect('/app/pedido/route/'+str(pedido.pk))
    except:
        messages.error(request, 'Este pedido foi deletado pela Loja')
        return HttpResponseRedirect('/app/pedidos/motorista/')


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
        print('>>>>>>>> Motorista '+pedido.motorista.first_name+' foi liberado pela loja '+pedido.estabelecimento.user.first_name)
        message = "Voce foi liberado pela loja para realizar a(s) entrega(s). Sua Rota atual esta no menu ENTREGAS. Quando terminar uma entrega, marque finalizar. Qualquer problema, ligue para a loja: " + pedido.estabelecimento.phone
        n = Notification(type_message='ENABLE_ROTA', to=pedido.motorista, message=message)
        n.save()
    return redirect('/app/acompanhar')
    

@require_http_methods(["GET"])
def finalizar_entrega(request, pk_ponto, pk_pedido):
    try:
        ponto = Ponto.objects.get(id=pk_ponto)
        pedido = Pedido.objects.get(id=pk_pedido)
        ponto.status = True
        ponto.save()
        pto_entregues = len(pedido.ponto_set.filter(status=True))
        print(len(pedido.ponto_set.all()) == pto_entregues)
        if len(pedido.ponto_set.all()) == pto_entregues:
            pedido.is_complete = True
            pedido.save()
            messages.success(request, 'Tudo entregue! Finalize este pedido para poder pegar outros.')
        if pedido.estabelecimento.is_online:
            print('>>>>>>>> Motorista '+request.user.first_name+' entregou pedido ao cliente '+ponto.cliente)
            message =  "Motorista "+request.user.first_name+" entregou pedido ao cliente "+ponto.cliente+ " no endereco "+ponto.full_address
            n = Notification(type_message='ORDER_DELIVERED', to=pedido.estabelecimento.user, message=message)
            n.save()
        return HttpResponseRedirect('/app/pedido/route/'+ str(pedido.pk))
    except:
        print('******* error url ')
        messages.error(request, 'Este pedido foi deletado pela Loja')
        return HttpResponseRedirect('/app/pedidos/motorista/')
    

@require_http_methods(["GET"])
def finalizar_pedido(request, pk_pedido):
    try:
        pedido = Pedido.objects.get(id=pk_pedido)
        pedido.btn_finalizado = True
        pedido.save()
        motorista = Motorista.objects.get(user=request.user)
        motorista.ocupado = False
        motorista.save()
        message = "O motorista " + request.user.first_name + " finalizou por completo a entrega do Pedido ID #" + str(
            pedido.pk) + ". Se desejar confirmar, ligue para o motorista: " + motorista.phone
        n = Notification(type_message='ALL_DELIVERED', to=pedido.estabelecimento.user, message=message)
        n.save()
        messages.success(request, 'Você concluiu a entrega do pedido, obrigado!')
        return HttpResponseRedirect('/app/pedidos/motorista/')
    except:
        messages.error(request, 'Este pedido foi deletado pela Loja')
        return HttpResponseRedirect('/app/pedidos/motorista/')
