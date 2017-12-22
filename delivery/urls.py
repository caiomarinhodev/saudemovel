"""urls.py: Urls definidas."""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views.HomeView import DashboardView
from app.views.MotoristasAtivosView import MotoristasAtivosView
from app.views.LoginView import LoginView, LogoutView, RegisterView, AppView
from app.views.LocationView import get_position_motorista, send_position_motorista
from app.views.pedidos.AcompanharView import AcompanharListView, AcompanharDetailView, LojasMotoristaListView
from app.views.pedidos.NotificationView import notificar_novo_pedido_motorista, notificar_delete_loja_motorista, \
    notificar_accept_order_loja, notificar_enable_rota_motorista, NotificacoesListView, notificar_all_delivered_loja, \
    notificar_admin_message
from app.views.pedidos.PedidoView import PedidosMotoristaListView, \
    PedidosLojaListView, PedidoCreateView, get_pedidos_motorista, accept_corrida, \
    EntregasMotoristaListView, get_entregas_motorista, delete_pedido, liberar_corrida, OrderMotoristaDetailView, \
    RouteMotoristaDetailView, MapRouteMotoristaView, finalizar_entrega, finalizar_pedido, PedidoUpdateView, cancel_pedido, \
    PedidoDetailView

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
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registro/$', RegisterView.as_view(), name='registro'),
    url(r'^account/logout/$', LogoutView.as_view(), name='auth_logout'),

    url(r'^app/pedidos/motorista/$', PedidosMotoristaListView.as_view(), name='pedidos_motorista'),
    url(r'^app/pedidos/loja/$', PedidosLojaListView.as_view(), name='pedidos_estabelecimento'),
    url(r'^app/pedidos/add/$', PedidoCreateView.as_view(), name='add_pedido'),
    url(r'^app/pedidos/(?P<pk>[0-9]+)/delete/$', delete_pedido, name='delete_pedido'),
    url(r'^app/pedidos/(?P<pk>[0-9]+)/cancel/$', cancel_pedido, name='cancel_pedido'),
    url(r'^app/pedido/(?P<pk>[0-9]+)/edit/$', PedidoUpdateView.as_view(), name="edit_pedido_view"),
    url(r'^app/pedido/(?P<pk>[0-9]+)/view/$', PedidoDetailView.as_view(), name="view_pedido_view"),
    url(r'^app/pedido/(?P<pk>[0-9]+)/$', OrderMotoristaDetailView.as_view(), name="order_pedido_view"),
    url(r'^app/pedido/route/(?P<pk>[0-9]+)/$', RouteMotoristaDetailView.as_view(), name="route_pedido_view"),
    url(r'^app/pedido/map/route/(?P<pk>[0-9]+)/$', MapRouteMotoristaView.as_view(), name="map_route_pedido_view"),
    url(r'^app/pedidos/motoristas/loja/$', MotoristasAtivosView.as_view(), name='motoristas_ativos_view'),

    url(r'^app/acompanhar/(?P<pk>[0-9]+)/$', AcompanharDetailView.as_view(), name="acompanhar_pedido_view"),
    url(r'^app/acompanhar/$', AcompanharListView.as_view(), name='acompanhar_list'),
    url(r'^app/lojas/$', LojasMotoristaListView.as_view(), name='lojas_credenciadas'),

    url(r'^get-pedidos/$', get_pedidos_motorista, name="get_pedidos_motorista"),

    url(r'^accept-corrida/(?P<pk_pedido>[0-9]+)/$', accept_corrida, name="accept_corrida"),

    url(r'^app/entregas/motorista/$', EntregasMotoristaListView.as_view(), name='entregas_motorista'),

    url(r'^get-entregas/$', get_entregas_motorista, name="get_entregas_motorista"),

    url(r'liberar-corrida/(?P<pk_pedido>[0-9]+)/$', liberar_corrida, name="liberar_corrida"),
    
    url(r'finalizar-entrega/(?P<pk_ponto>[0-9]+)/(?P<pk_pedido>[0-9]+)/$', finalizar_entrega, name="finalizar_entrega"),

    url(r'finalizar-pedido/(?P<pk_pedido>[0-9]+)/$', finalizar_pedido, name="finalizar_pedido"),
    
    url(r'send-location/(-?\d+\.\d+)/(-?\d+\.\d+)/$', send_position_motorista, name="send_position_motorista"),
    
    url(r'get-location/(?P<pk_user>[0-9]+)/$', get_position_motorista, name=" get_position_motorista"),


    url(r'^app/notificacoes/$', NotificacoesListView.as_view(), name='notificacoes'),
    url(r'^notificacao/novo-pedido/motorista/$', notificar_novo_pedido_motorista, name="notify_novo_pedido_motorista"),
    url(r'^notificacao/delete-loja/motorista/$', notificar_delete_loja_motorista, name="notify_delete_loja_motorista"),
    url(r'^notificacao/accept-order/loja/$', notificar_accept_order_loja, name="notify_accept_order_loja"),
    url(r'^notificacao/all-delivered/loja/$', notificar_all_delivered_loja, name="notificar_all_delivered_loja"),
    url(r'^notificacao/adminmessage$', notificar_admin_message, name="notify_admin_message"),
    url(r'^notificacao/enable-rota/motorista/$', notificar_enable_rota_motorista, name="notify_enable_rota_motorista"),
]
