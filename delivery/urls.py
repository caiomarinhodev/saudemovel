"""urls.py: Urls definidas."""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views.HomeView import AppView
from app.views.LoginView import LoginView, LogoutView
from app.views.pedidos.AcompanharView import AcompanharListView
from app.views.pedidos.NotificationView import notificar_novo_pedido_motorista, notificar_delete_loja_motorista, \
    notificar_accept_order_loja, notificar_cancel_order_loja, notificar_enable_rota_motorista, NotificacoesListView
from app.views.pedidos.PedidoView import PedidosMotoristaListView, \
    PedidosLojaListView, PedidoCreateView, get_pedidos_motorista, accept_corrida, cancel_corrida_motorista, \
    EntregasMotoristaListView, get_entregas_motorista, delete_pedido, liberar_corrida

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"

"""default URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),
    url(r'^$', AppView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^account/logout/$', LogoutView.as_view(), name='auth_logout'),

    url(r'^app/pedidos/motorista/$', PedidosMotoristaListView.as_view(), name='pedidos_motorista'),
    url(r'^app/pedidos/loja/$', PedidosLojaListView.as_view(), name='pedidos_estabelecimento'),
    url(r'^app/pedidos/add/$', PedidoCreateView.as_view(), name='add_pedido'),
    url(r'^app/pedidos/(?P<pk>[0-9]+)/delete/$', delete_pedido, name='delete_pedido'),

    url(r'^app/acompanhar/$', AcompanharListView.as_view(), name='acompanhar_list'),

    url(r'^get-pedidos/$', get_pedidos_motorista, name="get_pedidos_motorista"),

    url(r'^accept-corrida/(?P<pk_pedido>[0-9]+)/$', accept_corrida, name="accept_corrida"),

    url(r'^app/entregas/motorista/$', EntregasMotoristaListView.as_view(), name='entregas_motorista'),

    url(r'^get-entregas/$', get_entregas_motorista, name="get_entregas_motorista"),

    url(r'liberar-corrida/(?P<pk_pedido>[0-9]+)/$', liberar_corrida, name="liberar_corrida"),

    url(r'^cancel-corrida-motorista/(?P<pk_pedido>[0-9]+)/$', cancel_corrida_motorista,
        name="cancel_corrida_motorista"),

    url(r'^app/notificacoes/$', NotificacoesListView.as_view(), name='notificacoes'),
    url(r'^notificacao/novo-pedido/motorista/$', notificar_novo_pedido_motorista, name="notify_novo_pedido_motorista"),
    url(r'^notificacao/delete-loja/motorista/$', notificar_delete_loja_motorista, name="notify_delete_loja_motorista"),
    url(r'^notificacao/accept-order/loja/$', notificar_accept_order_loja, name="notify_accept_order_loja"),
    url(r'^notificacao/cancel-order/loja/$', notificar_cancel_order_loja, name="notify_cancel_order_loja"),
    url(r'^notificacao/enable-rota/motorista/$', notificar_enable_rota_motorista, name="notify_enable_rota_motorista"),
]
