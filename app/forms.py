#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, inlineformset_factory

from app.models import Pedido, Ponto, Estabelecimento, Motorista


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'


class FormBaseAddress(BaseForm):
    cep = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'required': True,
                                                                       'maxlength': 200,
                                                                       'placeholder': 'CEP'
                                                                       }))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    bairro = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                          'maxlength': 200,
                                                                          'placeholder': 'Bairro'
                                                                          }))


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))


class FormPedido(ModelForm, BaseForm):
    class Meta:
        model = Pedido
        fields = ['estabelecimento', 'is_draft']


class FormPonto(ModelForm, BaseForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'telefone',
                                                             'maxlength': 200,
                                                             'placeholder': 'Telefone do Cliente'}))
    cliente = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                            'maxlength': 200,
                                                            'placeholder': 'Nome do Cliente'}))

    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 6, 'class': 'numero',
                                                                         'placeholder': 'Número'
                                                                         }))
    complemento = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                                'maxlength': 200,
                                                                                'placeholder': 'Ponto de Referencia'
                                                                                }))
    observacoes = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'required': True,
                                                                                               'maxlength': 300,
                                                                                               'placeholder': 'Insira aqui as instrucoes de pagamento e o valor do pedido para ser coletado pelo motoboy'
                                                                                               }))

    class Meta:
        model = Ponto
        fields = ['telefone', 'cliente', 'endereco', 'numero', 'bairro', 'complemento', 'observacoes']


class FormEditPonto(ModelForm, BaseForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': False, 'class': 'telefone',
                                                             'maxlength': 200,
                                                             'placeholder': 'Telefone do Cliente'}))
    cliente = forms.CharField(widget=forms.TextInput(attrs={'required': False,
                                                            'maxlength': 200,
                                                            'placeholder': 'Nome do Cliente'}))

    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': False,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': False,
                                                                         'maxlength': 200, 'class': 'numero',
                                                                         'placeholder': 'Número'
                                                                         }))
    complemento = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': False,
                                                                                'maxlength': 200,
                                                                                'placeholder': 'Ponto de Referencia'
                                                                                }))
    observacoes = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'required': False,
                                                                                               'maxlength': 300,
                                                                                               'placeholder': 'Observações'
                                                                                               }))

    class Meta:
        model = Ponto
        fields = ['id', 'telefone', 'cliente', 'endereco', 'numero', 'bairro', 'complemento', 'observacoes']


class FormRegister(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Estabelecimento'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    endereco = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                            'maxlength': 200,
                                                                            'placeholder': 'Endereço'
                                                                            }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': True, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Estabelecimento
        fields = ['bairro', ]


class FormEditPerfil(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Estabelecimento'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    endereco = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                            'maxlength': 200,
                                                                            'placeholder': 'Endereço'
                                                                            }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': True, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Estabelecimento
        fields = ['bairro', ]


class FormMotoristaRegister(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Completo'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    cpf = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'required': True,
                                                                                       'maxlength': 200,
                                                                                       'placeholder': 'CPF'
                                                                                       }))
    placa = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'required': True,
                                                                                         'maxlength': 200,
                                                                                         'placeholder': 'Placa do Veiculo'
                                                                                         }))
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': False, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Motorista
        fields = []


PontoFormSet = inlineformset_factory(Pedido, Ponto, form=FormPonto, extra=1)

PontoFormUpdateSet = inlineformset_factory(Pedido, Ponto, form=FormEditPonto, extra=0)
