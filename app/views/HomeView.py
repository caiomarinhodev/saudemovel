#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import DashboardMixin, ListMotoristasMixin, DashboardListMixin
from app.models import ConfigAdmin

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class AppView(TemplateView):
    template_name = 'entrega/page/index.html'


class CollectView(TemplateView):
    template_name = 'entrega/page/collect.html'


class ContributeView(TemplateView):
    template_name = 'entrega/page/contribute.html'


class DashboardListPedidosView(LoginRequiredMixin, TemplateView, DashboardListMixin):
    login_url = '/login/'
    template_name = 'entrega/admin/list_pedidos.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/login')
        return super(DashboardListPedidosView, self).get(request, *args, **kwargs)


class DashboardDataView(LoginRequiredMixin, TemplateView, DashboardMixin):
    login_url = '/login/'
    template_name = 'entrega/admin/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/login')
        return super(DashboardDataView, self).get(request, *args, **kwargs)


class ListMotoristasView(LoginRequiredMixin, TemplateView, ListMotoristasMixin):
    login_url = '/login/'
    template_name = 'entrega/admin/list_motoristas.html'


def set_feriado_admin(request):
    config = ConfigAdmin.objects.first()
    config.is_feriado = not config.is_feriado
    config.save()
    return redirect('/app/dashboard/')
