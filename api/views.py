# Create your views here.
from rest_framework import generics
from rest_framework import viewsets

from api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class BairroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bairro.objects.all().order_by('nome')
    serializer_class = BairroSerializer


class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


class EstabelecimentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Estabelecimento.objects.all().order_by('-created_at')
    serializer_class = EstabelecimentoFullSerializer


class EstabelecimentoList(generics.ListAPIView):
    queryset = Estabelecimento.objects.all()
    serializer_class = EstabelecimentoFullSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Pedido.objects.all().order_by('-created_at')
    serializer_class = PedidoSerializer


class PontoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Ponto.objects.all().order_by('-created_at')
    serializer_class = PontoSerializer
