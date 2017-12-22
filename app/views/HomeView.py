#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.CustomContextMixin import DashboardMixin

from app.models import Pedido

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class AppView(TemplateView):
    template_name = 'page/index.html'


class CollectView(TemplateView):
    template_name = 'page/collect.html'


class ContributeView(TemplateView):
    template_name = 'page/contribute.html'


class DashboardView(LoginRequiredMixin, TemplateView, DashboardMixin):
    template_name = 'dashboard.html'