from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import DetailView

from app.models import Pedido


class AcompanharListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'acompanhar/list_acompanhar_loja.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user, status=False).order_by('-created_at')


class AcompanharDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/acompanhar_view.html'
    context_object_name = 'pedido'