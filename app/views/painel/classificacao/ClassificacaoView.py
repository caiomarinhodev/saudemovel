from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import Categoria, Avaliacao
from app.views.mixins.Mixin import FocusMixin


class ClassificacaoListView(LoginRequiredMixin, ListView, FocusMixin):
    template_name = 'painel/classificacao/list.html'
    login_url = '/loja/login/'
    context_object_name = 'classificacoes'
    model = Avaliacao
    ordering = '-created_at'

    def get_queryset(self):
        est = self.request.user.estabelecimento
        return Avaliacao.objects.filter(estabelecimento=est)
