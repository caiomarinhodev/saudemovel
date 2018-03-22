from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import Categoria, Avaliacao, Notificacao
from app.views.mixins.Mixin import FocusMixin


class NotificacaoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/notificacao/list.html'
    login_url = '/painel/login'
    context_object_name = 'notificacoes'
    model = Notificacao
    ordering = '-created_at'

    def get_queryset(self):
        return Notificacao.objects.filter(to=self.request.user)
