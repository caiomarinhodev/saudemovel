from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormGrupo, OpcionalFormSet, OpcionalUpdateFormSet
from app.models import Grupo
from app.views.mixins.Mixin import FocusMixin
from app.views.script_tools import logger


class GrupoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/grupo/list.html'
    login_url = '/loja/login/'
    context_object_name = 'grupos'
    model = Grupo
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Grupo.objects.filter(produto__categoria__estabelecimento=est)


class GrupoCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/loja/login/'
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
        try:
            logger(self.request.user, "Criou o grupo " + str(self.object))
        except (Exception,):
            pass
        context = self.get_context_data()
        print(context)
        opcionalset = context['opcionalset']
        with transaction.atomic():
            self.object = form.save()
            if opcionalset.is_valid():
                opcionalset.instance = self.object
                opcionalset.save()
        return super(GrupoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(GrupoCreateView, self).form_invalid(form)


class GrupoUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/loja/login/'
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
        try:
            logger(self.request.user, "Alterou o grupo " + str(self.object))
        except (Exception,):
            pass
        context = self.get_context_data()
        print(context)
        opcionalset = context['opcionalset']
        with transaction.atomic():
            self.object = form.save()
            if opcionalset.is_valid():
                opcionalset.instance = self.object
                opcionalset.save()
        return super(GrupoUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(GrupoUpdateView, self).form_invalid(form)


class GrupoDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'grupo'
    model = Grupo
    success_url = '/grupo/list'
    template_name = 'painel/grupo/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            logger(self.request.user, "Deletou o grupo " + str(self.object))
        except (Exception,):
            pass
        return super(GrupoDeleteView, self).post(request, *args, **kwargs)
