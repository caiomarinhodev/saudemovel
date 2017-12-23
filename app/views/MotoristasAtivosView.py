#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.mixins.CustomContextMixin import CustomContextMixin
from app.models import Pedido


class MotoristasAtivosView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos/list_motoristas_ativos.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user, is_complete=False).order_by('-created_at')
