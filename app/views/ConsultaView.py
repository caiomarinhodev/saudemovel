#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.models import Consulta

"""ConsultaView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class ConsultaListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'sistema/consulta/list.html'
    model = Consulta
    context_object_name = 'consultas'
    ordering = '-created_at'


class ConsultaCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'sistema/consulta/add.html'
    context_object_name = 'consulta'
    fields = ('paciente', 'especialista', 'data', 'local', 'cidade',)
    model = Consulta
    success_url = '/'


class ConsultaUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'sistema/consulta/edit.html'
    model = Consulta
    context_object_name = 'consulta'
    fields = ('paciente', 'especialista', 'data', 'local', 'cidade', )
    success_url = '/'
