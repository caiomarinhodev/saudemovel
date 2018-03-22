from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormGrupo, OpcionalFormSet, OpcionalUpdateFormSet
from app.models import Grupo
from app.views.mixins.Mixin import FocusMixin


class GrupoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/grupo/list.html'
    login_url = '/painel/login'
    context_object_name = 'grupos'
    model = Grupo
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Grupo.objects.filter(produto__categoria__estabelecimento=est)


class GrupoCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'grupo'
    model = Grupo
    success_url = '/grupo/list'
    template_name = 'painel/grupo/add.html'
    form_class = FormGrupo

    def get_context_data(self, **kwargs):
        data = super(GrupoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['opcionalset'] = OpcionalFormSet(self.request.POST)
        else:
            data['opcionalset'] = OpcionalFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        opcionalset = context['opcionalset']
        with transaction.atomic():
            self.object = form.save()
            if opcionalset.is_valid():
                opcionalset.instance = self.object
                opcionalset.save()
        # message = "Um novo pedido foi feito pela " + self.request.user.first_name
        # print('>>>>>>>> Novo Pedido criado pela loja ' + self.request.user.first_name)
        # pedido = self.object
        # if not pedido.is_draft:
        #     a = func()
        #     for m in Motorista.objects.all():
        #         if m.is_online and not m.ocupado:
        #             n = Notification(type_message='NOVO_PEDIDO', to=m.user, message=message)
        #             n.save()
        return super(GrupoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(GrupoCreateView, self).form_invalid(form)


class GrupoUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'grupo'
    model = Grupo
    success_url = '/grupo/list'
    template_name = 'painel/grupo/edit.html'
    form_class = FormGrupo

    def get_context_data(self, **kwargs):
        data = super(GrupoUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['opcionalset'] = OpcionalUpdateFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['opcionalset'] = OpcionalUpdateFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        opcionalset = context['opcionalset']
        with transaction.atomic():
            self.object = form.save()
            if opcionalset.is_valid():
                opcionalset.instance = self.object
                opcionalset.save()
        # message = "Um novo pedido foi feito pela " + self.request.user.first_name
        # print('>>>>>>>> Novo Pedido criado pela loja ' + self.request.user.first_name)
        # pedido = self.object
        # if not pedido.is_draft:
        #     a = func()
        #     for m in Motorista.objects.all():
        #         if m.is_online and not m.ocupado:
        #             n = Notification(type_message='NOVO_PEDIDO', to=m.user, message=message)
        #             n.save()
        return super(GrupoUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(GrupoUpdateView, self).form_invalid(form)


class GrupoDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'grupo'
    model = Grupo
    success_url = '/grupo/list'
    template_name = 'painel/grupo/delete.html'
