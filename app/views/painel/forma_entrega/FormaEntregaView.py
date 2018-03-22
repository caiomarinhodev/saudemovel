from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormFormaEntrega
from app.models import FormaEntrega
from app.views.mixins.Mixin import FocusMixin


class FormaEntregaListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/forma_entrega/list.html'
    login_url = '/painel/login'
    context_object_name = 'formas'
    model = FormaEntrega
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return FormaEntrega.objects.filter(estabelecimento=est)


class FormaEntregaCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'formaentrega'
    model = FormaEntrega
    success_url = '/entrega/list'
    template_name = 'painel/forma_entrega/add.html'
    form_class = FormFormaEntrega

    def get_initial(self):
        return {'estabelecimento': self.request.user.estabelecimento}


class FormaEntregaUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'formaentrega'
    model = FormaEntrega
    success_url = '/entrega/list'
    template_name = 'painel/forma_entrega/edit.html'
    form_class = FormFormaEntrega

    def get_initial(self):
        return {'estabelecimento': self.request.user.estabelecimento}


class FormaEntregaDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'formaentrega'
    model = FormaEntrega
    success_url = '/entrega/list'
    template_name = 'painel/forma_entrega/delete.html'
