# coding=utf-8
from django.views.generic.base import ContextMixin
from django.contrib import messages
from django.views.generic import ListView
from app.models import *
from django.shortcuts import redirect
from django.contrib.auth import logout


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
        try:
            motorista = Motorista.objects.get(user=self.request.user)
            if not motorista.is_approved:
                motorista.is_online = False
                motorista.save()
                logout(self.request)
        except:
            pass
        if 'notifications_n' not in kwargs:
            kwargs['notifications_n'] = Notification.objects.filter(to=self.request.user, is_read=False).order_by(
                '-created_at')

        try:
            if 'messages_e' not in kwargs:
                kwargs['messages_e'] = Message.objects.filter(u_to=self.request.user, is_read=False)
            if 'pedidos_n' not in kwargs:
                kwargs['pedidos_n'] = Pedido.objects.filter(estabelecimento=self.request.user.estabelecimento,
                                                            status=False, is_complete=False).order_by(
                    '-created_at')
                kwargs['motoristas_online'] = Motorista.objects.filter(is_online=True, ocupado=False)
                print(kwargs['motoristas_online'])
                kwargs['pedidos_andamento'] = Pedido.objects.filter(estabelecimento=self.request.user.estabelecimento,
                                                                    status=False, is_complete=False,
                                                                    coletado=True).order_by(
                    '-created_at')
                kwargs['pedidos_pendentes'] = Pedido.objects.filter(estabelecimento=self.request.user.estabelecimento,
                                                                    status=True, is_complete=False,
                                                                    coletado=False).order_by(
                    '-created_at')

        except:
            if 'messages_m' not in kwargs:
                kwargs['messages_m'] = Message.objects.filter(u_to=self.request.user, is_read=False)
            if 'pedidos_n' not in kwargs:
                kwargs['pedidos_n'] = Pedido.objects.filter(motorista=self.request.user, status=False,
                                                            is_complete=False).order_by(
                    '-created_at')
        return super(CustomContextMixin, self).get_context_data(**kwargs)


class DashboardMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        motoristas = Motorista.objects.all()
        pedidos = Pedido.objects.all()
        users = User.objects.all()
        notificacoes = Notification.objects.all()
        locations = Location.objects.all()
        bairros = Bairro.objects.all()
        estabelecimentos = Estabelecimento.objects.all()
        pontos = Ponto.objects.all()
        kwargs['motoristas'] = motoristas
        kwargs['pedidos'] = pedidos
        kwargs['users'] = users
        kwargs['estabelecimentos'] = estabelecimentos
        kwargs['bd_space'] = float(float(float(
            len(motoristas) + len(pedidos) + len(users) + len(notificacoes) + len(locations) + len(bairros) + len(
                estabelecimentos) + len(pontos)) / 10000) * 100)
        kwargs['pedidos_entregues'] = Pedido.objects.filter(is_complete=True)
        kwargs['pedidos_pendentes'] = Pedido.objects.filter(status=True)
        kwargs['pedidos_andamento'] = Pedido.objects.filter(status=False, is_complete=False)
        kwargs['motoristas_online'] = Motorista.objects.filter(is_online=True)
        kwargs['motoristas_livres'] = Motorista.objects.filter(is_online=True, ocupado=False)
        kwargs['motoristas_ocupados'] = Motorista.objects.filter(is_online=True, ocupado=True)
        return super(DashboardMixin, self).get_context_data(**kwargs)
