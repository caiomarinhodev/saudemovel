# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime, time

from django.contrib.auth.models import User
from django.db import models

from app.views.geocoding import geocode


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class Bairro(TimeStamped):
    nome = models.CharField(max_length=100, blank=True)
    valor = models.CharField(max_length=3, blank=True, null=True)
    valor_madrugada = models.CharField(max_length=3, default='8')
    valor_madrugada_feriado = models.CharField(max_length=3, default='11')
    valor_feriado = models.CharField(max_length=3, default='9')

    def __unicode__(self):
        return u'%s' % self.nome

    def __str__(self):
        return u'%s' % self.nome


class BaseAddress(models.Model):
    class Meta:
        abstract = True

    bairro = models.ForeignKey(Bairro, blank=True, null=True, verbose_name='Bairro')
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ponto de Referência')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)


class Motorista(TimeStamped, BaseAddress):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    cpf = models.CharField(max_length=100, blank=True, null=True, default="")
    photo = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    ocupado = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    placa = models.CharField(max_length=30, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        super(Motorista, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name

    def __unicode__(self):
        return u'%s' % self.user.first_name


class ConfigAdmin(TimeStamped):
    is_feriado = models.BooleanField(default=False)


THEMES = (
    ('BLACK', 'skin-black'),
    ('BLUE', 'skin-blue'),
    ('RED', 'skin-red'),
    ('YELLOW', 'skin-yellow'),
    ('PURPLE', 'skin-purple'),
    ('GREEN', 'skin-green'),
    # 'skin-blue-light',
    # 'skin-black-light',
    # 'skin-red-light',
    # 'skin-yellow-light',
    # 'skin-purple-light',
    # 'skin-green-light'
)

PLANS = (
    ('BASIC', 'BASIC'),
    ('PREMIUM', 'PREMIUM'),
)


class Configuration(TimeStamped):
    tema = models.CharField(max_length=100, blank=True, null=True, choices=THEMES, default='skin-black')
    plano = models.CharField(max_length=100, choices=PLANS, default='BASIC')


class Estabelecimento(TimeStamped, BaseAddress):
    configuration = models.OneToOneField(Configuration, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_approved = models.BooleanField(default=False)
    photo = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    is_online = models.BooleanField(default=False)
    full_address = models.CharField(max_length=300, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            self.numero = self.numero.replace("_", "")
            self.phone = self.phone.replace("_", "")
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            self.full_address = address
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        super(Estabelecimento, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user.first_name

    def __str__(self):
        return u'%s' % self.user.first_name

    class Meta:
        permissions = (
            ("view_dashboard_1", "Loja pode ver o dashboard loja tipo 1"),
            ("view_dashboard_2", "Loja pode ver o dashboard loja tipo 2"),
            ("view_dashboard_3", "Loja pode ver o dashboard loja tipo 3"),
            ("view_chat", "Loja pode interagir no Chat"),
        )


class Pedido(TimeStamped):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    coletado = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    valor_total = models.CharField(max_length=6)
    btn_finalizado = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False, )
    motorista = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.estabelecimento, self.valor_total)

    def __str__(self):
        return u'%s - %s' % (self.estabelecimento, self.valor_total)

    def save(self, *args, **kwargs):
        config = ConfigAdmin.objects.first()
        valor = 0
        for pto in self.ponto_set.all():
            now = datetime.now()
            now_time = now.time()
            if config.is_feriado:
                if time(22, 59) <= now_time <= time(23, 59):
                    valor = valor + int(pto.bairro.valor_madrugada_feriado)
                elif time(0, 00) <= now_time <= time(5, 59):
                    valor = valor + int(pto.bairro.valor_madrugada_feriado)
                else:
                    valor = valor + int(pto.bairro.valor_feriado)
            else:
                if time(22, 59) <= now_time <= time(23, 59):
                    valor = valor + int(pto.bairro.valor_madrugada)
                elif time(0, 00) <= now_time <= time(5, 59):
                    valor = valor + int(pto.bairro.valor_madrugada)
                else:
                    valor = valor + int(pto.bairro.valor)
        self.valor_total = valor
        super(Pedido, self).save(*args, **kwargs)


class Ponto(BaseAddress, TimeStamped):
    cliente = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    full_address = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=False)
    duration = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            self.numero = self.numero.replace("_", "")
            self.telefone = self.telefone.replace("_", "")
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
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
    ('ADMIN_MESSAGE', 'ADMIN_MESSAGE'),
    ('ALL_DELIVERED', 'ALL_DELIVERED'),
    ('LOJA_MESSAGE', 'LOJA_MESSAGE'),
    ('MOTORISTA_MESSAGE', 'MOTORISTA_MESSAGE')
)


class Notification(TimeStamped):
    message = models.TextField()
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    type_message = models.CharField(choices=type_notification, max_length=100)
    is_read = models.BooleanField(default=False)


class Message(TimeStamped):
    u_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_from')
    u_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_to')
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)


class Location(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)


class Classification(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nota = models.CharField(max_length=2)
