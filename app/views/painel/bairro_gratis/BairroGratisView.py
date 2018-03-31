from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from app.forms import FormBairroGratis
from app.models import Estabelecimento, BairroGratis
from app.views.mixins.Mixin import FocusMixin
from app.views.script_tools import logger


class BairroGratisListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/bairro_gratis/list.html'
    login_url = '/painel/login'
    context_object_name = 'bairros'
    model = BairroGratis
    ordering = '-created_at'

    def get_queryset(self):
        est = Estabelecimento.objects.get(user=self.request.user)
        return BairroGratis.objects.filter(estabelecimento=est)


class BairroGratisCreateView(LoginRequiredMixin, CreateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'bairro'
    model = BairroGratis
    success_url = '/bairro/list'
    template_name = 'painel/bairro_gratis/add.html'
    form_class = FormBairroGratis

    def get_initial(self):
        return {'estabelecimento': self.request.user.estabelecimento}

    def form_valid(self, form):
        try:
            logger(self.request.user, "Criou a Bairro Gratis #" + str(self.object.pk))
        except (Exception,):
            pass
        return super(BairroGratisCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(BairroGratisCreateView, self).form_invalid(form)


class BairroGratisUpdateView(LoginRequiredMixin, UpdateView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'bairro'
    model = BairroGratis
    success_url = '/bairro/list'
    template_name = 'painel/bairro_gratis/edit.html'
    form_class = FormBairroGratis

    def get_initial(self):
        return {'estabelecimento': self.request.user.estabelecimento}

    def form_valid(self, form):
        try:
            logger(self.request.user, "Editou a Bairro Gratis #" + str(self.object.pk))
        except (Exception,):
            pass
        return super(BairroGratisUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(BairroGratisUpdateView, self).form_invalid(form)


class BairroGratisDeleteView(LoginRequiredMixin, DeleteView, FocusMixin):
    login_url = '/painel/login'
    context_object_name = 'bairro_gratis'
    model = BairroGratis
    success_url = '/bairro/list'
    template_name = 'painel/bairro_gratis/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            logger(self.request.user, "Deletou a Bairro Gratis #" + str(self.object.pk))
        except (Exception,):
            pass
        return super(BairroGratisDeleteView, self).post(request, *args, **kwargs)
