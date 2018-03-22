from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context
from django.views.decorators.http import require_http_methods

from app.models import Notificacao, Pedido, Request, Ponto, Notification
from app.views.fcm import func
from app.views.snippet_template import render_block_to_string


@require_http_methods(["GET"])
def notificacao_pedido(request):
    notificacao = Notificacao.objects.filter(to=request.user, type_message='NOVO_PEDIDO', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('painel/includes/notificacao.html', context)
    # Nao marcar como lido. Marcar somente depois que aceitar ou rejeitar.
    # if notificacao:
    #     notificacao.is_read = True
    #     notificacao.save()
    return HttpResponse(return_str)


def mark_read(request):
    notificacao = Notificacao.objects.filter(to=request.user, type_message='NOVO_PEDIDO', is_read=False).last()
    if notificacao:
        notificacao.is_read = True
        notificacao.save()


def aceitar_pedido(request, pk):
    mark_read(request)
    req = Request.objects.get(id=pk)
    req.status_pedido = 'ACEITO'
    req.save()
    pedido = Pedido(estabelecimento=req.estabelecimento, valor_total=req.endereco_entrega.bairro.valor)
    pedido.save()
    ponto = Ponto(pedido=pedido,
                  cliente=unicode(req.cliente.usuario.first_name) + u" " + unicode(req.cliente.usuario.last_name),
                  telefone=req.cliente.telefone, observacoes=" ", itens=" *** ")
    ponto.save()
    a = func()
    no = Notification(type_message='NOTIFICACAO_COZINHA', to=request.user, message='NOVO PEDIDO REALIZADO')
    no.save()
    return redirect('/dashboard')


def rejeitar_pedido(request, pk):
    mark_read(request)
    pedido = Request.objects.get(id=pk)
    pedido.status_pedido = 'REJEITADO'
    pedido.save()
    return redirect('/dashboard')
