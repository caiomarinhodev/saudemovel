# coding=utf-8
from django.views.generic.base import ContextMixin
from django.contrib import messages
from django.views.generic import ListView
from app.models import Motorista, Notification, Pedido
from django.shortcuts import redirect
#

class RedirectMotoristaOcupadoView(ListView):
    def get(self, request, *args, **kwargs):
        motorista = None
        try:
            motorista = Motorista.objects.get(user=self.request.user)
        except:
            pass
        if motorista:
            if motorista.ocupado:
                return redirect('entregas_motorista')
        return super(RedirectMotoristaOcupadoView, self).get(request, *args, **kwargs)

class CustomContextMixin(ContextMixin):
     def get_context_data(self, **kwargs):
        if 'notifications_n' not in kwargs:
             kwargs['notifications_n'] = Notification.objects.filter(to=self.request.user, is_read=False).order_by('-created_at')
        try:
            if 'pedidos_n' not in kwargs:
                 kwargs['pedidos_n'] = Pedido.objects.filter(estabelecimento=self.request.user.estabelecimento, status=False, is_complete=False).order_by(
                     '-created_at')
        except:
             if 'pedidos_n' not in kwargs:
                 kwargs['pedidos_n'] = Pedido.objects.filter(motorista=self.request.user, status=False, is_complete=False).order_by(
                     '-created_at')
        return super(CustomContextMixin, self).get_context_data(**kwargs)
