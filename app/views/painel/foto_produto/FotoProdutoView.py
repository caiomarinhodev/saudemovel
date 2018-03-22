from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormFotoProduto
from app.models import FotoProduto
from app.views.mixins.Mixin import FocusMixin


class FotoProdutoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/foto_produto/list.html'
    login_url = '/painel/login'
    context_object_name = 'fotos'
    model = FotoProduto
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return FotoProduto.objects.filter(produto__categoria__estabelecimento=est)


class FotoProdutoCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'foto'
    model = FotoProduto
    success_url = '/opcional/list'
    template_name = 'painel/foto_produto/add.html'
    form_class = FormFotoProduto


class FotoProdutoUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'foto'
    model = FotoProduto
    success_url = '/opcional/list'
    template_name = 'painel/foto_produto/edit.html'
    form_class = FormFotoProduto


class FotoProdutoDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'foto'
    model = FotoProduto
    success_url = '/opcional/list'
    template_name = 'painel/foto_produto/delete.html'
