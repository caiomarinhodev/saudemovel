#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView, DetailView

from app.models import ItemPedido, Opcional, OpcionalChoice, Cliente, Request, Estabelecimento, Produto, Endereco, \
    Bairro, FormaPagamento, FormaEntrega, Notificacao
from app.views.mixins.Mixin import LojaFocusMixin


def check_same_store(id_loja, pedido):
    if int(id_loja) == int(pedido.estabelecimento.id):
        return True
    return False


def cria_item_pedido(checks, pedido, produto, obs):
    itempedido = ItemPedido(pedido=pedido, quantidade='1', produto=produto, observacoes=obs)
    itempedido.save()
    for id in checks:
        opc = Opcional.objects.get(id=id)
        print(u'%s' % opc)
        opcc = OpcionalChoice(opcional=opc, item_pedido=itempedido)
        opcc.save()
    itempedido.save()


def is_logged(request):
    try:
        if request.user:
            cliente = Cliente.objects.get(usuario=request.user)
            if cliente:
                return True
            else:
                return False
        else:
            return False
    except (Exception,):
        return False


def get_pedido(request, id_loja):
    try:
        return Request.objects.get(id=request.session['pedido'])
    except (Exception,):
        estabelecimento = Estabelecimento.objects.get(id=id_loja)
        pedido = Request(cliente=request.user.cliente, estabelecimento=estabelecimento)
        pedido.save()
        request.session['pedido'] = pedido.id
        print('SESSION PEDIDO: ' + str(request.session['pedido']))
        return pedido


def add_cart(request, id_loja):
    print('loja: ' + str(id_loja))
    if is_logged(request):
        checks = request.POST.getlist('checks')
        print('--------------')
        pedido = get_pedido(request, id_loja)
        print('teste: ' + str(pedido.estabelecimento.id))
        print('check: ' + str(check_same_store(id_loja, pedido)))
        print('produton in : ' + str('produto' in request.POST))
        if check_same_store(id_loja, pedido) and ('produto' in request.POST):
            produto = Produto.objects.get(id=request.POST['produto'])
            obrigatorios = produto.grupo_set.filter(obrigatoriedade=True)
            if check_required_selected(checks, obrigatorios) or obrigatorios.count() == 0:
                obs = request.POST['observacoes']
                cria_item_pedido(checks, pedido, produto, obs)
            else:
                messages.error(request, u'Você deve selecionar 1 item das opcoes com *(asterisco)')
        else:
            messages.error(request, u'Você deve comprar produtos no mesmo estabelecimento')
            return redirect('/loja/' + str(pedido.estabelecimento.id))
        pedido.save()
        print('loja: ' + str(id_loja))
        return redirect('/loja/' + str(pedido.estabelecimento.id))
    messages.error(request, u'Para fazer um pedido você deve estar logado')
    return redirect('/define/login/')


def remove_cart(request, pk):
    pedido = Request.objects.get(id=request.session['pedido'])
    id_loja = pedido.estabelecimento.id
    print(request.session)
    del request.session['pedido']
    print(request.session)
    pedido.delete()
    messages.success(request, 'Pedido deletado com sucesso')
    return redirect('/loja/' + str(id_loja))  # redirecionar para a loja


def check_required_selected(checks, list):
    for group in list:
        if group:
            for check in checks:
                opc = Opcional.objects.filter(id=check).first()
                if opc.grupo.id == group.id:
                    return True
            return False
        else:
            return True


def check_loja_is_online(request):
    loja = Request.objects.get(id=request.session['pedido']).estabelecimento
    return loja.is_online


class FinalizaRequest(LoginRequiredMixin, TemplateView, LojaFocusMixin):
    template_name = 'loja/finaliza_pedido.html'
    login_url = '/define/login/'

    def get(self, request, *args, **kwargs):
        if not check_loja_is_online(self.request):
            messages.error(self.request, u'A Loja não está mais online para receber pedidos.')
            return redirect('/')
        return super(FinalizaRequest, self).get(request, *args, **kwargs)


def submit_pedido(request):
    data = request.POST
    cliente = request.user.cliente
    pedido = Request.objects.get(id=request.session['pedido'])
    troco = None
    endereco = None
    print(data)
    if 'endereco' in data:
        if data['endereco'] != '':
            endereco = Endereco.objects.get(id=data['endereco'])
            endereco.save()
    else:
        if ('bairro' in data) and ('rua' in data) and ('numero' in data) and ('complemento' in data):
            if (data['bairro'] != u'') and (data['rua'] != u'' and (data['numero'] != u'')):
                bairro = Bairro.objects.get(id=data['bairro'])
                endereco = Endereco(cliente=cliente, bairro=bairro, endereco=data['rua'], numero=data['numero'],
                                    complemento=data['complemento'])
                endereco.save()
        else:
            messages.error(request, u'Selecione o endereco de entrega ou Informe o endereco de entrega')
            return redirect('/finaliza-pedido/')
    if 'pgto' in data:
        if data['pgto'] != u'':
            forma_pagamento = FormaPagamento.objects.get(id=data['pgto'])
            print(forma_pagamento)
            if forma_pagamento.forma == 'DINHEIRO':
                if 'troco' in data:
                    if data['troco'] != u'':
                        pedido.troco = data['troco']
                    else:
                        messages.error(request, u'Insira o valor do Troco')
                        return redirect('/finaliza-pedido/')
                else:
                    messages.error(request, u'Insira o valor do Troco')
                    return redirect('/finaliza-pedido/')
    else:
        messages.error(request, u'Insira uma forma de pagamento')
        return redirect('/finaliza-pedido/')
    # if 'entrega' in data:
    #     forma_entrega = FormaEntrega.objects.get(id=data['entrega'])
    # else:
    #     messages.error(request, u'Defina uma forma de entrega')
    #     return redirect('/finaliza-pedido/')
    if 'troco' in data:
        if data['troco'] != u'':
            pedido.troco = data['troco']
    pedido.forma_pagamento = forma_pagamento
    # pedido.forma_entrega = forma_entrega
    if endereco:
        pedido.endereco_entrega = endereco
    else:
        messages.error(request, u'Selecione o endereco de entrega ou Informe o endereco de entrega')
        return redirect('/finaliza-pedido/')
    pedido.save()
    messages.success(request, 'Pedido Realizado com Sucesso')
    message = make_message(pedido)
    n = Notificacao(type_message='NOVO_PEDIDO', to=pedido.estabelecimento.user, message=message, pedido=pedido)
    n.save()
    return redirect('/acompanhar-pedido/' + str(pedido.pk))


def make_message(pedido):
    message = u'Cliente: ' + unicode(pedido.cliente.usuario.first_name) + u' ' + unicode(
        pedido.cliente.usuario.last_name) + u' ' + u'Telefone: ' + unicode(
        pedido.cliente.telefone) + u' ' + u'Pedido:' + u' '
    for it in pedido.itempedido_set.all():
        message += u' ' + unicode(it.produto.nome) + u'('
        for opc in it.opcionalchoice_set.all():
            message += unicode(opc.opcional.nome) + u','
        message += u') '
    return message


class AcompanharRequest(LoginRequiredMixin, DetailView):
    template_name = 'loja/acompanha_pedido.html'
    login_url = '/define/login/'
    model = Request
    context_object_name = 'pedido_obj'

    def get(self, request, *args, **kwargs):
        if 'pedido' in self.request.session:
            del self.request.session['pedido']
        return super(AcompanharRequest, self).get(request, *args, **kwargs)


class MeusRequests(LoginRequiredMixin, TemplateView, LojaFocusMixin):
    template_name = 'loja/meus_pedidos.html'
    login_url = '/define/login/'
