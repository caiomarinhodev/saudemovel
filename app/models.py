# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class BaseAddress(models.Model):
    class Meta:
        abstract = True

    cep = models.CharField(max_length=15, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, verbose_name='Bairro')
    endereco = models.CharField(max_length=100, blank=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=200, blank=True, verbose_name='Ponto de Referência')


class Motorista(TimeStamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    photo = models.URLField(blank=True)
    phone = models.CharField(max_length=30)
    ocupado = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    def __unicode__(self):
        return u'%s' % self.user.first_name


class Estabelecimento(TimeStamped, BaseAddress):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    photo = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_online = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.user.first_name

    def __str__(self):
        return u'%s' % self.user.first_name


class Pedido(TimeStamped):
    nome_cliente = models.CharField(max_length=100)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    coletado = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    valor_total = models.CharField(max_length=6)
    motorista = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.nome_cliente

    def __str__(self):
        return self.nome_cliente


class Ponto(BaseAddress, TimeStamped):
    descricao = models.TextField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    # status = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.endereco

    def __str__(self):
        return self.endereco


class Position(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)
    lat_map = models.CharField(max_length=100)
    lng_map = models.CharField(max_length=100)
