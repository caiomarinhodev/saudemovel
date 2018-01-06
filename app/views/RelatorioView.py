from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import CustomContextMixin


class RelatorioTemplateView(LoginRequiredMixin, TemplateView, CustomContextMixin):
    login_url = '/login/'
    template_name = 'reports/relatorios_base.html'
