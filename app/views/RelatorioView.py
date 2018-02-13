from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import CustomContextMixin
from app.models import Pedido, Motorista


class RelatorioTemplateView(LoginRequiredMixin, TemplateView, CustomContextMixin):
    login_url = '/login/'
    template_name = 'reports/relatorios_base.html'


class DashboardReportViewUser(LoginRequiredMixin, TemplateView, CustomContextMixin):
    login_url = '/login/'
    template_name = 'admin/ver_relatorios_loja.html'

    # def get_context_data(self, **kwargs):
    #     kwargs['user'] = User.objects.get(id=self.request.GET['pk'])
    #     return super(DashboardReportViewUser, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        kwargs['user'] = User.objects.get(id=self.request.GET['pk'])
        return super(DashboardReportViewUser, self).get(request, *args, **kwargs)


class TimelineView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login'
    template_name = 'reports/timeline.html'
    model = Pedido
    context_object_name = 'rotas'

    def get_queryset(self):
        now = datetime.now()
        return Pedido.objects.filter(is_draft=False, created_at__day=now.day).order_by('-created_at')


class PromocaoListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    template_name = 'promo/list_motoristas.html'
    model = Motorista
    context_object_name = 'motoristas'

    def get_queryset(self):
        return Motorista.objects.all()
