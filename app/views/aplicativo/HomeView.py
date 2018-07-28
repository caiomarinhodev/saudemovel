#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from app.models import Consulta


class ListConsultas(LoginRequiredMixin, ListView):
    login_url = '/aplicativo/login/'
    template_name = 'app_template/wish-list.html'
    context_object_name = 'consultas'
    model = Consulta

    def get_queryset(self):
        est = Consulta.objects.filter(paciente__user=self.request.user).order_by('?')
        return est


class ConsultaView(LoginRequiredMixin, DetailView):
    login_url = '/aplicativo/login/'
    template_name = 'app_template/product-detail.html'
    context_object_name = 'consulta'
    model = Consulta
    pk_url_kwarg = 'pk'
