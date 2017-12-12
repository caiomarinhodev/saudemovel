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
from django.views.generic import ListView

from app.forms import PontoFormSet
from app.models import Pedido, Estabelecimento, Motorista
from app.views.snippet_template import render_block_to_string


class PedidosLojaListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos/list_pedidos_loja.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user).order_by('-created_at')


class PedidosMotoristaListView(LoginRequiredMixin, ListView):
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
    fields = ['estabelecimento', 'valor_total']
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
        # TODO: Implementar sistema para notificar Motorista de que Novo Pedido foi adicionado. BIPAR em todos.
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
        pedido.delete()
        # TODO: Implementar sistema para notificar Motorista que A Coleta/Pedido dele foi cancelada/deletado pela Loja.
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
        # TODO: Notificar a loja de que UM motorista aceitou fazer a entrega do pedido X e esta a caminho.
        return redirect('/app/entregas/motorista')


@require_http_methods(["GET"])
def cancel_corrida(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    pedido.status = True
    pedido.motorista = None
    pedido.is_complete = False
    pedido.coletado = False
    pedido.save()
    motorista = Motorista.objects.get(user=request.user)
    motorista.ocupado = False
    motorista.save()
    # TODO: Implementar sistema que notifica a loja de que O motorista cancelou a entrega, e o pedido esta disponivel.
    return redirect('/app/pedidos/motorista')

# TODO: Implementar botao em acompanhamentos da loja para liberar pedido para entrega.
# TODO: Motorista ao logar, ao sair da page qualquer e estiver OCUPADO(entregando), notificar o endereco da entrega e redirecionar para /entregas
# TODO: Implementar botao em acompanhamentos da loja para liberar pedido para entrega.
# TODO: Implementar botao em acompanhamentos da loja para acompanhar entrega, apos liberado.
# TODO: Implementar notificacao p/ motorista de que o produto foi liberado para entrega, e mostrar rota(mapa).
# TODO: Notificar Loja de que motorista X saiu para entrega e pode ser acompanhado em acompanhamentos id #.
# TODO: Implementar botao de Finalizar Entrega em entregas do motorista, para finalizar uma entrega.
# TODO: Implementar notificacao p/ loja de que o produto foi entregue.

