from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormCategoria, ProdutoFormSet
from app.models import Categoria, Estabelecimento
from app.views.mixins.Mixin import FocusMixin


class CategoriaListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/categoria/list_categoria.html'
    login_url = '/loja/login/'
    context_object_name = 'categorias'
    model = Categoria
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Categoria.objects.filter(estabelecimento=est)


class CategoriaCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'categoria'
    form_class = FormCategoria
    model = Categoria
    success_url = '/categoria/list/'
    template_name = 'painel/categoria/add_categoria.html'

    def get_context_data(self, **kwargs):
        data = super(CategoriaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            print(self.request.POST)
            data['produtoset'] = ProdutoFormSet(self.request.POST)
        else:
            data['produtoset'] = ProdutoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        produtoset = context['produtoset']
        with transaction.atomic():
            self.object = form.save()
            if produtoset.is_valid():
                produtoset.instance = self.object
                produtoset.save()
        return super(CategoriaCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CategoriaCreateView, self).form_invalid(form)

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }


class CategoriaUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'categoria'
    model = Categoria
    form_class = FormCategoria
    success_url = '/categoria/list'
    template_name = 'painel/categoria/edit_categoria.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }

    def get_context_data(self, **kwargs):
        data = super(CategoriaUpdateView, self).get_context_data(**kwargs)
        print(self.request.POST)
        if self.request.POST:
            data['produtoset'] = ProdutoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['produtoset'] = ProdutoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        produtoset = context['produtoset']
        with transaction.atomic():
            self.object = form.save()
            if produtoset.is_valid():
                produtoset.instance = self.object
                produtoset.save()
        return super(CategoriaUpdateView, self).form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'categoria'
    model = Categoria
    success_url = '/categoria/list'
    template_name = 'painel/categoria/delete_categoria.html'
