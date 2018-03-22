from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormFormaPagamento
from app.models import FormaPagamento, Estabelecimento
from app.views.mixins.Mixin import FocusMixin


class FormaPagamentoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/forma_pagamento/list.html'
    login_url = '/painel/login'
    context_object_name = 'formas'
    model = FormaPagamento
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return FormaPagamento.objects.filter(estabelecimento=est)


class FormaPagamentoCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'formapagamento'
    model = FormaPagamento
    success_url = '/pagamento/list'
    template_name = 'painel/forma_pagamento/add.html'
    form_class = FormFormaPagamento

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class FormaPagamentoUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'formapagamento'
    model = FormaPagamento
    success_url = '/pagamento/list'
    template_name = 'painel/forma_pagamento/edit.html'
    form_class = FormFormaPagamento

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class FormaPagamentoDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'formapagamento'
    model = FormaPagamento
    success_url = '/pagamento/list'
    template_name = 'painel/forma_pagamento/delete.html'
