from base64 import b64encode

import pyimgur
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormProduto, GrupoFormSet, FotoProdutoFormSet, GrupoUpdateFormSet, FotoProdutoUpdateFormSet
from app.models import Produto, Estabelecimento, FotoProduto
from app.views.mixins.Mixin import FocusMixin
from app.views.script_tools import logger


class ProdutoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/produto/list.html'
    login_url = '/painel/login'
    context_object_name = 'produtos'
    model = Produto
    ordering = '-created_at'

    def get_queryset(self):
        est = Estabelecimento.objects.get(user=self.request.user)
        return Produto.objects.filter(categoria__estabelecimento=est)


class ProdutoCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'produto'
    model = Produto
    success_url = '/produto/list'
    template_name = 'painel/produto/add.html'
    form_class = FormProduto

    def get_context_data(self, **kwargs):
        data = super(ProdutoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['gruposet'] = GrupoFormSet(self.request.POST)
            data['fotoset'] = FotoProdutoFormSet(self.request.POST)
        else:
            data['gruposet'] = GrupoFormSet()
            data['fotoset'] = FotoProdutoFormSet()
        return data

    def form_valid(self, form):
        try:
            logger(self.request.user, "Criou o produto " + str(self.object))
        except (Exception,):
            pass
        context = self.get_context_data()
        print(context)
        gruposet = context['gruposet']
        fotoset = context['fotoset']
        with transaction.atomic():
            self.object = form.save()
            if gruposet.is_valid():
                gruposet.instance = self.object
                gruposet.save()
            if fotoset.is_valid():
                fotoset.instance = self.object
                fotoset.save()
        # message = "Um novo pedido foi feito pela " + self.request.user.first_name
        # print('>>>>>>>> Novo Pedido criado pela loja ' + self.request.user.first_name)
        # pedido = self.object
        # if not pedido.is_draft:
        #     a = func()
        #     for m in Motorista.objects.all():
        #         if m.is_online and not m.ocupado:
        #             n = Notification(type_message='NOVO_PEDIDO', to=m.user, message=message)
        #             n.save()
        return super(ProdutoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ProdutoCreateView, self).form_invalid(form)


class ProdutoUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'produto'
    model = Produto
    success_url = '/produto/list'
    template_name = 'painel/produto/edit.html'
    form_class = FormProduto

    def get_context_data(self, **kwargs):
        data = super(ProdutoUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['gruposet'] = GrupoUpdateFormSet(self.request.POST, self.request.FILES, instance=self.object)
            data['fotoset'] = FotoProdutoUpdateFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['gruposet'] = GrupoUpdateFormSet(instance=self.object)
            data['fotoset'] = FotoProdutoUpdateFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        try:
            logger(self.request.user, "Alterou o produto " + str(self.object))
        except (Exception,):
            pass
        context = self.get_context_data()
        print(context)
        gruposet = context['gruposet']
        fotoset = context['fotoset']
        with transaction.atomic():
            self.object = form.save()
            if gruposet.is_valid():
                gruposet.instance = self.object
                gruposet.save()
            if fotoset.is_valid():
                # for form in fotoset.cleaned_data:
                #     if 'file' in form:
                #         if form['file']:
                fotoset.instance = self.object
                fotoset.save()
        # message = "Um novo pedido foi feito pela " + self.request.user.first_name
        # print('>>>>>>>> Novo Pedido criado pela loja ' + self.request.user.first_name)
        # pedido = self.object
        # if not pedido.is_draft:
        #     a = func()
        #     for m in Motorista.objects.all():
        #         if m.is_online and not m.ocupado:
        #             n = Notification(type_message='NOVO_PEDIDO', to=m.user, message=message)
        #             n.save()
        return super(ProdutoUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ProdutoUpdateView, self).form_invalid(form)


class ProdutoDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'produto'
    model = Produto
    success_url = '/produto/list'
    template_name = 'painel/produto/delete.html'
