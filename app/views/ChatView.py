from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic import TemplateView

from app.models import Pedido, Message, Motorista, Estabelecimento, Notification
from app.views.snippet_template import render_block_to_string


class ListChatView(LoginRequiredMixin, TemplateView):
    template_name = 'pedidos/list_all_chats.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        kwargs['pedidos'] = Pedido.objects.filter(estabelecimento__user=self.request.user, status=False,
                                                  is_complete=False)
        return super(ListChatView, self).get_context_data(**kwargs)


class ChatPedidoView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/chat.html'
    login_url = '/login'


class ChatMotoristaPedidoView(LoginRequiredMixin, TemplateView):
    template_name = 'pedidos/chat.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        kwargs['pedido'] = Pedido.objects.filter(motorista=self.request.user, status=False, is_complete=False).last()
        return super(ChatMotoristaPedidoView, self).get_context_data(**kwargs)


@require_http_methods(["GET"])
def get_chat(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    messages = pedido.message_set.all().order_by('created_at')
    for m in messages:
        if not m.is_read:
            m.is_read = True
            m.save()
    for n in Notification.objects.filter(to=request.user, is_read=False, message="Nova Mensagem"):
        n.is_read = True
        n.save()
    context = Context({'pedido': pedido, 'user': request.user, 'messages': messages})
    return_str = render_block_to_string('includes/messages.html', context)
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def return_to_get_chat(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    messages = pedido.message_set.all().order_by('created_at')
    context = Context({'pedido': pedido, 'user': request.user, 'messages': messages})
    return_str = render_block_to_string('includes/messages.html', context)
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def submit_message(request, pk_pedido):
    text = request.GET['text']
    motorista = None
    pedido = Pedido.objects.get(id=pk_pedido)
    loja = None
    try:
        motorista = Motorista.objects.get(user=request.user)
    except:
        loja = Estabelecimento.objects.get(user=request.user)
    if motorista:
        mess = Message(u_from=motorista.user, u_to=pedido.estabelecimento.user, text=text, pedido=pedido, is_read=False)
        mess.save()
        message = "Nova Mensagem"
        n = Notification(type_message='MOTORISTA_MESSAGE', to=pedido.estabelecimento.user, message=message)
        n.save()
    elif loja:
        mess = Message(u_from=loja.user, u_to=pedido.motorista, text=text, pedido=pedido, is_read=False)
        mess.save()
        message = "Nova Mensagem"
        n = Notification(type_message='LOJA_MESSAGE', to=pedido.motorista, message=message)
        n.save()
    return return_to_get_chat(request, pedido.pk)
