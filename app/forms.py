#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,}))


class FormLoginCliente(BaseForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 12,
                                                             'placeholder': 'Telefone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
