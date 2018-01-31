#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import FormPontoCliente
from app.mixins.CustomContextMixin import CustomContextMixin
from app.models import Ponto


class ClientesListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Ponto
    context_object_name = 'clientes'
    template_name = 'clientes/list_clientes.html'

    def get_queryset(self):
        return Ponto.objects.filter(Q(pedido__estabelecimento=self.request.user.estabelecimento) | Q(
            estabelecimento=self.request.user.estabelecimento)).order_by(
            '-created_at')


class ClienteCreateView(LoginRequiredMixin, CreateView, CustomContextMixin):
    model = Ponto
    success_url = '/app/clientes/'
    form_class = FormPontoCliente
    template_name = 'clientes/cliente.html'

    def form_valid(self, form):
        loja = self.request.user.estabelecimento
        self.object = form.save()
        pto = self.object
        pto.estabelecimento = loja
        pto.save()
        return super(ClienteCreateView, self).form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView, CustomContextMixin):
    model = Ponto
    success_url = '/app/clientes/'
    form_class = FormPontoCliente
    template_name = 'clientes/cliente.html'
