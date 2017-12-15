# coding=utf-8
from django.views.generic.base import ContextMixin
from django.contrib import messages
from django.views.generic import ListView
from app.models import Motorista
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
                print(motorista)
                messages.error(request, "Você ainda não finalizou sua ultima rota!")
                return redirect('entregas_motorista')
        return super(RedirectMotoristaOcupadoView, self).get(request, *args, **kwargs)

class CustomContextMixin(ContextMixin):
     def get_context_data(self, **kwargs):
        #  if 'audits_l' not in kwargs:
        #      kwargs['audits_l'] = Audit.objects.filter(new_owner=self.request.user, is_complete=False,
        #                                               is_deferred='EM ANÁLISE').order_by('-created_at')
        #  if 'notifications_l' not in kwargs:
        #      kwargs['notifications_l'] = Notification.objects.filter(user=self.request.user, is_read=False).order_by(
        #          '-created_at')
         return super(CustomContextMixin, self).get_context_data(**kwargs)
#
#
# class UserContextMixin(ContextMixin):
#     def get_context_data(self, **kwargs):
#         if 'audits_for_user' not in kwargs:
#             kwargs['audits_for_user'] = Audit.objects.filter(donor=self.request.user,
#                                                              is_deferred='EM ANÁLISE').order_by('-created_at')
#         return super(UserContextMixin, self).get_context_data(**kwargs)
