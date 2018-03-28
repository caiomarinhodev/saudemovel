from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormChamado
from app.models import Categoria, Estabelecimento, Chamado
from app.views.mixins.Mixin import FocusMixin


class ChamadoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/chamado/list.html'
    login_url = '/loja/login'
    context_object_name = 'chamados'
    model = Chamado
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Chamado.objects.filter(estabelecimento=est)


class ChamadoCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'chamado'
    form_class = FormChamado
    model = Chamado
    success_url = '/chamado/list'
    template_name = 'painel/chamado/add.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class ChamadoUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/loja/login'
    context_object_name = 'chamado'
    model = Chamado
    form_class = FormChamado
    success_url = '/chamado/list'
    template_name = 'painel/chamado/edit.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class ChamadoDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/loja/login'
    context_object_name = 'chamado'
    model = Chamado
    success_url = '/chamado/list'
    template_name = 'painel/chamado/delete.html'
