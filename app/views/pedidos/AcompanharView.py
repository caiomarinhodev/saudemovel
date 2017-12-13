from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import Pedido


class AcompanharListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'acompanhar/list_acompanhar_loja.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user, status=False).order_by('-created_at')
