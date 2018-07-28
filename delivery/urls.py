"""urls.py: Urls definidas."""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views.ConsultaView import ConsultaListView, ConsultaCreateView, ConsultaUpdateView
from app.views.LoginView import LogoutView, LoginAtendenteView
from app.views.aplicativo.HomeView import ListConsultas, ConsultaView
from app.views.aplicativo.LoginView import LoginView, LogoutAppView

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, EMPSOFT-UFCG"

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
    url(r'^$', ConsultaListView.as_view(), name='consultas'),
    url(r'^login/$', LoginAtendenteView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='auth_logout'),
    url(r'^consulta/add/$', ConsultaCreateView.as_view(), name='add_consulta'),
    url(r'^consulta/edit/(?P<pk>[0-9]+)/$', ConsultaUpdateView.as_view(), name='edit_consulta'),
    url(r'^consulta/list/$', ConsultaListView.as_view(), name='list_consulta'),

    # --------------------------------------------------------------------------
    url(r'^aplicativo/$', ListConsultas.as_view(), name='home_app'),
    url(r'^aplicativo/consulta/$', ListConsultas.as_view(), name='home_app'),
    url(r'^aplicativo/login/$', LoginView.as_view(), name='login_app'),
    url(r'^aplicativo/logout/$', LogoutAppView.as_view(), name='logout_app'),
    url(r'^aplicativo/consulta/(?P<pk>[0-9]+)/$', ConsultaView.as_view(), name='view_consulta_app'),
]
