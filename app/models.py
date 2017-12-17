# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from app.views.geocoding import geocode


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class BaseAddress(models.Model):
    class Meta:
        abstract = True

    nome_cliente = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cliente')
    bairro = models.CharField(max_length=100, blank=True, verbose_name='Bairro')
    endereco = models.CharField(max_length=100, blank=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=200, blank=True, verbose_name='Ponto de Referência')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)


class Motorista(TimeStamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    photo = models.URLField(blank=True)
    phone = models.CharField(max_length=30)
    ocupado = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    placa = models.CharField(max_length=30)

    def __str__(self):
        return self.user.first_name

    def __unicode__(self):
        return u'%s' % self.user.first_name


class Estabelecimento(TimeStamped, BaseAddress):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    photo = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_online = models.BooleanField(default=False)
    full_address = models.CharField(max_length=300, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        self.numero = self.numero.replace("_", "")
        self.phone = self.phone.replace("_", "")
        address = self.endereco + "," + self.bairro + ",Campina Grande,PB"
        self.full_address = address
        pto = geocode(address)
        self.lat = pto['latitude']
        self.lng = pto['longitude']
        super(Estabelecimento, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user.first_name

    def __str__(self):
        return u'%s' % self.user.first_name


class Pedido(TimeStamped):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    coletado = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    valor_total = models.CharField(max_length=6)
    btn_finalizado = models.BooleanField(default=False)
    motorista = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.estabelecimento, self.valor_total)

    def __str__(self):
        return u'%s - %s' % (self.estabelecimento, self.valor_total)
        
    def save(self, *args, **kwargs):
        valor = str(len(self.ponto_set.all()) * 6)
        self.valor_total = valor
        super(Pedido, self).save(*args, **kwargs)


class Ponto(BaseAddress, TimeStamped):
    cliente = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    full_address = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.numero = self.numero.replace("_", "")
        self.telefone = self.telefone.replace("_", "")
        address = self.endereco + "," + self.bairro + ",Campina Grande,PB"
        pto = geocode(address)
        self.lat = pto['latitude']
        self.lng = pto['longitude']
        self.full_address = address
        super(Ponto, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.endereco

    def __str__(self):
        return self.endereco


type_notification = (
    ('NOVO_PEDIDO', 'NOVO_PEDIDO'),
    ('DELETE_LOJA', 'DELETE_LOJA'),
    ('ACCEPT_ORDER', 'ACCEPT_ORDER'),
    ('CANCEL_ORDER', 'CANCEL_ORDER'),
    ('ENABLE_ROTA', 'ENABLE_ROTA'),
    ('ORDER_DELIVERED', 'ORDER_DELIVERED'),
    ('ALL_DELIVERED', 'ALL_DELIVERED')
)

class Notification(TimeStamped):
    message = models.TextField()
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    type_message = models.CharField(choices=type_notification, max_length=100)
    is_read = models.BooleanField(default=False)


class Location(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)