from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormCategoria
from app.models import Categoria, Estabelecimento
from app.views.mixins.Mixin import FocusMixin


class CategoriaListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/categoria/list_categoria.html'
    login_url = '/painel/login'
    context_object_name = 'categorias'
    model = Categoria
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Categoria.objects.filter(estabelecimento=est)


class CategoriaCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/login/'
    context_object_name = 'categoria'
    form_class = FormCategoria
    model = Categoria
    success_url = '/categoria/list'
    template_name = 'painel/categoria/add_categoria.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class CategoriaUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'categoria'
    model = Categoria
    form_class = FormCategoria
    success_url = '/categoria/list'
    template_name = 'painel/categoria/edit_categoria.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class CategoriaDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'categoria'
    model = Categoria
    success_url = '/categoria/list'
    template_name = 'painel/categoria/delete_categoria.html'
