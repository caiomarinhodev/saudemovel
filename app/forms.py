#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, inlineformset_factory, formset_factory

from app.models import Pedido, Ponto


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FormBaseAddress(BaseForm):
    cep = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'CEP'
    }))
    endereco = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
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
        fields = ['status', 'estabelecimento', 'valor_total']


class FormPonto(ModelForm, BaseForm):
    class Meta:
        model = Ponto
        fields = ['cliente', 'endereco', 'numero', 'bairro', 'complemento', 'descricao']
        

class FormRegister(FormBaseAddress):
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
    
    


PontoFormSet = inlineformset_factory(Pedido, Ponto, form=FormPonto, extra=1)
