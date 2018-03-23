#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic import RedirectView

from app.models import Estabelecimento, Bairro
from app.views.mixins.Mixin import LojaFocusMixin


class HomeView(ListView, LojaFocusMixin):
    template_name = 'loja/index.html'
    context_object_name = 'lojas'
    model = Estabelecimento

    def get_context_data(self, **kwargs):
        kwargs['lojas_off'] = Estabelecimento.objects.filter(is_online=False).order_by('?')
        return super(HomeView, self).get_context_data(**kwargs)

    def get_queryset(self):
        est = Estabelecimento.objects.filter(is_online=True).order_by('?')
        return est


class LojaProdutosListView(DetailView, LojaFocusMixin):
    template_name = 'loja/view_produtos.html'
    context_object_name = 'loja'
    model = Estabelecimento
    pk_url_kwarg = 'pk'


class SetOnlineView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user:
            loja = Estabelecimento.objects.get(user=self.request.user)
            loja.is_online = not loja.is_online
            loja.save()
            return '/dashboard'
        else:
            return '/define/login/'


def script(request):
    list_names = ['Acacio Figueiredo',
                  'Alameda',
                  'Alto Branco',
                  'Araxa',
                  'Bairro das Cidades',
                  'Bairro das Nacoes',
                  'Bairro Universitario',
                  'Bela Vista',
                  'Bodocongo',
                  'Caatingueira',
                  'Catole',
                  'Centenario',
                  'Centro',
                  'Cinza',
                  'Conceicao',
                  'Cruzeiro',
                  'Cuites',
                  'Dinamerica',
                  'Distrito Industrial',
                  'Estacao Velha',
                  'Gloria',
                  'Itarare',
                  'Jardim Continental',
                  'Jardim Paulistano',
                  'Jardim Tavares',
                  'Jardim Verdejante',
                  'Jeremias',
                  'Joao Paulo II',
                  'Jose Pinheiro',
                  'Lauritzen',
                  'Liberdade',
                  'Ligeiro',
                  'Louzeiro',
                  'Major Veneziano',
                  'Malvinas',
                  'Mirante',
                  'Monte Castelo',
                  'Monte Santo',
                  'Nova Brasilia',
                  'Novo Bodocongo',
                  'Novo Cruzeiro',
                  'Novo Horizonte',
                  'Palmeira',
                  'Palmeira Imperial',
                  'Pedregal',
                  'Portal Sudoeste',
                  'Prata',
                  'Presidente Medici',
                  'Quarenta',
                  'Ramadinha',
                  'Rocha Cavalcante',
                  'Rosa Cruz',
                  'Sandra Cavalcante',
                  'Santa Cruz',
                  'Santa Rosa',
                  'Santo Antonio',
                  'Sao Jose',
                  'Serrotao',
                  'Severino Cabral',
                  'Tambor',
                  'Tres Irmas',
                  'Velame',
                  'Vila Cabral de Santa Rosa',
                  'Vila Cabral de Santa Terezinha']
    for name in list_names:
        b = Bairro(nome=name)
        b.save()
    return redirect('/')

    # Refactor HomeView (10min) OK
    # Implementar check na obrigatoriedade no backend (20min) OK
    # Implementar Sistema para ficar ONLINE/OFFLINE (30min) OK
    # Implementar JS check de obrigatoriedade no grupo  (15min) OK
    # Implementar botao para Finalizar Pedido (10 min) OK
    # Implementar Verificacao no back com messages se Loja is Online apos clicar no botao Finalizar Pedido (30min) OK
    # Implementar tela de inserir dados de entrega,  (1h30) OK

    # Implementar valor em Bairro. Prepopular bairros no banco. (30min) OK
    # Implementar subtotal e calculos no model Pedido. (30min)  OK
    # Implementar atualizacao de total em finalizar entrega subtotal + entrega. (20min) OK
    # Implementar conclusao e submissao de Pedido pelo cliente. (45min) OK
    # Implementar Notificacao de Pedido para Loja (painel)  (1h30) OK

    # Link no Menu para Focus Geral (10min) OK
    # Inserir carrinho com redirect para as compras do Usuario; (50min) OK
    # Implementar tela de Acompanhar Pedido. (2h) OK
    # Implementar tela de Meus Pedidos (1h) OK
    # Implementar tela de Ver Pedido Realizado (30min) OK

    # Bug: Pode Alterar valor do bairro por JS na compra. OK
    # Bug: SEM CONTROLE SE PERMANECER NESSA GAMBIARRA. OK
    # Implementar Lançamento de Pedido para Focus Geral (3h30) OK
    # Implementar Alerta na Cozinha da Focus Geral (2h) OK
    # Implementar Check de enviar pedido se e sommente se loja ONLINE. (10min) OK
    # Implementar Aceitar, Rejeitar Pedido com set na tela de acompanhar pedido (2h) OK
    # Implementar Online/Offline do motoboy(1h) OK
    # Implementar CRUD de Pedido (30min) OK
    # Implementar Configuracao de Loja (1h) OK
    # Mostrar nome da loja estilo popup ao passar mouse sobre a foto da loja na HOME (30min) OK
    # Mostrar motoboy estilo perfil na tela de acompanhar entrega (45min) OK
    # Implementar Random na vitrine de lojas Online (1h) OK
    # Menu Pagamentos com tabela de Pagamentos e Opcao de Pagar (btn pagseguro ou api) OK

    # Texto Page Sobre Nós (menu link) (50min)
    # Aplicativo (menu link) (45 min)
    # Implementar Relatorios Simples no Dashboard para a Loja, de Vendas (1h45min)
