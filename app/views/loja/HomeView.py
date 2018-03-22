#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic import RedirectView

from app.models import Estabelecimento, Bairro
from app.views.mixins.Mixin import LojaFocusMixin


class HomeView(ListView, LojaFocusMixin):
    template_name = 'loja/index.html'
    context_object_name = 'lojas'
    model = Estabelecimento

    def get_queryset(self):
        return Estabelecimento.objects.all()


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
            return '/define/login'


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

# Bug: Pode Alterar valor do bairro por JS na compra.
# Bug: SEM CONTROLE SE PERMANECER NESSA GAMBIARRA.

# Implementar Aceitar, Rejeitar Pedido com set na tela de acompanhar pedido (2h)
# Implementar Configuracao de Loja (1h)
# Implementar Check de enviar pedido se e sommente se loja ONLINE. (10min)
# Implementar Random na vitrine de lojas Online (1h)
# Implementar Relatorios Simples no Dashboard para a Loja, de Vendas (45min)
# Implementar Lançamento de Pedido para Focus Geral (3h30)
# Implementar Alerta na Cozinha da Focus Geral (2h) OK

# Implementar API (20h)

# ---------------------------------------
# Apos as sucessivas adicoes no carrinho, o cliente vai para a tela de inserir dados de entrega,
# completa o pedido e envia -> tela de acompanhar pedido
# notificar loja, e aceitacao e rejeicao atualizar tela de acompanhar pedido.
# limpar sessao, no fim;

# As Lojas tem Configuracao na Focus. Se possui conta no Geral (lança pedido no sistema e pra
# COZINHA), Private.
# Em Configuração, deve haver Tempo de preparo. Endereço da Loja. Telefone. CNPJ.
# DEVE HAVER NO DASHBOARD UM BOTAO PARA FICAR ONLINE E OFFLINE;

# O botao de enviar pedido só deve aparecer se a loja estiver ONLINE

# Implementar a notificacao do Motoboy, placa e informacoes dele para o Cliente que pediu. (8h)

# Configuracao Loja: login,senha focus geral; foto; primeiro e ultimo nome; cnpj; notificar cozinha boolean; chamar motoboy boolean;