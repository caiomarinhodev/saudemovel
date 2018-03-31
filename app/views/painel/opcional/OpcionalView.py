from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.forms import FormOpcional
from app.models import Opcional
from app.views.mixins.Mixin import FocusMixin
from app.views.script_tools import logger


class OpcionalListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/opcional/list.html'
    login_url = '/loja/login/'
    context_object_name = 'opcionais'
    model = Opcional
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Opcional.objects.filter(grupo__produto__categoria__estabelecimento=est)


class OpcionalCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'opcional'
    model = Opcional
    success_url = '/opcional/list'
    template_name = 'painel/opcional/add.html'
    form_class = FormOpcional

    def form_valid(self, form):
        try:
            logger(self.request.user, "Criou o opcional " + str(self.object))
        except (Exception,):
            pass
        return super(OpcionalCreateView, self).form_valid(form)


class OpcionalUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'opcional'
    model = Opcional
    success_url = '/opcional/list'
    template_name = 'painel/opcional/edit.html'
    form_class = FormOpcional

    def form_valid(self, form):
        try:
            logger(self.request.user, "Editou o opcional " + str(self.object))
        except (Exception,):
            pass
        return super(OpcionalUpdateView, self).form_valid(form)


class OpcionalDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/loja/login/'
    context_object_name = 'opcional'
    model = Opcional
    success_url = '/opcional/list'
    template_name = 'painel/opcional/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            logger(self.request.user, "Deletou o opcional " + str(self.object))
        except (Exception,):
            pass
        return super(OpcionalDeleteView, self).post(request, *args, **kwargs)
