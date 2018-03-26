from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView

from app.forms import FormRequest, GrupoUpdateFormSet, ItemPedidoFormSet
from app.models import Notificacao, Pedido, Request, Ponto, Notification, FolhaPagamento, ItemPagamento
from app.views.fcm import func
from app.views.snippet_template import render_block_to_string
from app.views.script_tools import logger


@require_http_methods(["GET"])
def notificacao_pedido(request):
    notificacao = Notificacao.objects.filter(to=request.user, type_message='NOVO_PEDIDO', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('painel/includes/notificacao.html', context)
    # Nao marcar como lido. Marcar somente depois que aceitar ou rejeitar.
    # if notificacao:
    #     notificacao.is_read = True
    #     notificacao.save()
    return HttpResponse(return_str)


def mark_read(request):
    notificacao = Notificacao.objects.filter(to=request.user, type_message='NOVO_PEDIDO', is_read=False).last()
    if notificacao:
        notificacao.is_read = True
        notificacao.save()


def get_or_create_rota(req):
    rotas = Pedido.objects.filter(coletado=False, status_cozinha=False, estabelecimento=req.estabelecimento)
    if rotas:
        return rotas.last()
    else:
        rota = Pedido(estabelecimento=req.estabelecimento, valor_total=req.endereco_entrega.bairro.valor)
        rota.save()
        return rota


def make_itens(req):
    message = '<p><ul>'
    try:
        for it in req.itempedido_set.all():
            message += '<li>' + str(it.produto.nome) + '  ('
            for opc in it.opcionalchoice_set.all():
                message += str(opc.opcional.nome) + ','
            message += ') </li>'
        message += '</ul></p>'
    except (Exception,):
        for it in req.itempedido_set.all():
            message += '<li>' + unicode(it.produto.nome) + '  ('
            for opc in it.opcionalchoice_set.all():
                message += unicode(opc.opcional.nome) + ','
            message += ') </li>'
        message += '</ul></p>'
    return message


def make_obs(req):
    message = '<p><ul>'
    try:
        message += '<li>Forma de Pagamento: ' + str(req.forma_pagamento) + ' </li>'
        message += '<li>Valor Total: ' + str(req.valor_total) + ' </li>'
        message += '<li>Troco para: ' + str(req.forma_pagamento) + ' (' + str(req.resultado_troco) + ')</li>'
        message += '</ul></p>'
    except (Exception,):
        message += '<li>Forma de Pagamento: ' + unicode(req.forma_pagamento) + ' </li>'
        message += '<li>Valor Total: ' + unicode(req.valor_total) + ' </li>'
        message += '<li>Troco para: ' + unicode(req.forma_pagamento) + ' (' + unicode(req.resultado_troco) + ')</li>'
        message += '</ul></p>'

    return message


def get_or_create_folha(now, est):
    qs = FolhaPagamento.objects.filter(created_at__month=now.month, created_at__year=now.year, estabelecimento=est,
                                       status_pagamento=False)
    if qs:
        return qs.first()
    else:
        folha = FolhaPagamento(valor_total=' ', estabelecimento=est)
        folha.save()
        return folha


def aceitar_pedido(request, pk):
    mark_read(request)
    req = Request.objects.get(id=pk)
    req.status_pedido = 'ACEITO'
    req.save()
    logger(request.user, "Aceitou o pedido " + str(req))
    folha_pag = get_or_create_folha(datetime.now(), req.estabelecimento)
    item_pag = ItemPagamento(request=req, folha=folha_pag)
    item_pag.save()
    folha_pag.save()
    pedido = get_or_create_rota(req)
    pedido.save()
    if request.user.estabelecimento.configuration.chamar_motoboy:
        req.pedido = pedido
        itens = make_itens(req)
        obs = make_obs(req)
        ponto = Ponto(pedido=pedido, bairro=req.endereco_entrega.bairro, endereco=req.endereco_entrega.endereco,
                      numero=req.endereco_entrega.numero, complemento=req.endereco_entrega.complemento,
                      cliente=str(req.cliente.usuario.first_name) + " " + str(req.cliente.usuario.last_name),
                      telefone=req.cliente.telefone, observacoes=obs, itens=itens)
        req.save()
        ponto.save()
        pedido.save()
        # a = func()
    if request.user.estabelecimento.configuration.has_cozinha:
        no = Notification(type_message='NOTIFICACAO_COZINHA', to=request.user, message='NOVO PEDIDO REALIZADO')
        no.save()
    return redirect('/dashboard')


def chamar_motoboy(request, pk):
    pedido = Pedido.objects.get(id=pk)
    a = func()
    pedido.chamar_motoboy = False
    pedido.save()
    messages.success(request, 'Enviamos um chamado para o motoboy mais proximo')
    return redirect('/app/pedidos/loja/')


def chamar_motoboy_cozinha(request, pk):
    pedido = Pedido.objects.get(id=pk)
    a = func()
    pedido.chamar_motoboy = False
    pedido.save()
    messages.success(request, 'Enviamos um chamado para o motoboy mais proximo')
    return redirect('/app/cozinha/')


def rejeitar_pedido(request, pk):
    mark_read(request)
    pedido = Request.objects.get(id=pk)
    pedido.status_pedido = 'REJEITADO'
    pedido.save()
    logger(request.user, "Rejeitou o pedido " + str(pedido))
    return redirect('/dashboard')


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    context_object_name = 'pedido'
    login_url = '/loja/login/'
    success_url = '/dashboard/'
    template_name = 'painel/request/edit.html'
    form_class = FormRequest

    def get_context_data(self, **kwargs):
        data = super(RequestUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itempedido_set'] = ItemPedidoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['itempedido_set'] = ItemPedidoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        logger(self.request.user, "Aceitou o pedido " + str(self.object))
        context = self.get_context_data()
        itempedido_set = context['itempedido_set']
        with transaction.atomic():
            self.object = form.save()
            if itempedido_set.is_valid():
                itempedido_set.instance = self.object
                itempedido_set.save()
        return super(RequestUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RequestUpdateView, self).form_invalid(form)
