from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import FolhaPagamento, PagamentoMotorista


class PagamentoMotoboyListView(LoginRequiredMixin, ListView):
    template_name = 'entrega/pagamento_motorista/list.html'
    model = FolhaPagamento
    context_object_name = 'pagamentos'

    def get_queryset(self):
        queryset = PagamentoMotorista.objects.filter(motorista=self.request.user.motorista).order_by(
            '-created_at')
        return queryset
