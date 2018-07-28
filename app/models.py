# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class Addressable(models.Model):
    class Meta:
        abstract = True

    bairro = models.CharField(max_length=300, blank=True, null=True, verbose_name='Bairro')
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    cidade = models.CharField(max_length=300, blank=True, null=True)
    estado = models.CharField(max_length=300, blank=True, null=True)
    complemento = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ponto de Referência')


class Perfil(TimeStamped, Addressable):
    class Meta:
        abstract = True

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    data_nascimento = models.DateTimeField()
    telefone = models.CharField(max_length=300, blank=True, null=True)
    foto = models.URLField(blank=True, null=True, default='https://www.civilsociety.co.uk/assets/img/user-img-lg.jpg')


class Paciente(Perfil):
    cpf = models.CharField(max_length=300, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Atendente(Perfil):
    horario = models.CharField(max_length=300, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Especialista(Perfil):
    crm = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Consulta(TimeStamped):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    data = models.DateTimeField()
    local = models.CharField(max_length=300, blank=True, null=True)
    cidade = models.CharField(max_length=300, blank=True, null=True)


class Atestado(TimeStamped):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    data = models.DateTimeField()
    descricao = models.TextField()


class Prontuario(TimeStamped):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    data = models.DateTimeField()
    local = models.CharField(max_length=300, blank=True, null=True)
    cidade = models.CharField(max_length=300, blank=True, null=True)
    cid = models.CharField(max_length=10, blank=True, null=True, verbose_name='CID')
