from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import FolhaPagamento


class PagamentoListView(LoginRequiredMixin, ListView):
    template_name = 'painel/pagamento/list.html'
    model = FolhaPagamento
    context_object_name = 'pagamentos'

    def get_queryset(self):
        queryset = FolhaPagamento.objects.filter(estabelecimento=self.request.user.estabelecimento).order_by('-created_at')
        return queryset
