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
    cep = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
    }))
    address = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
    }))
    number = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={
    }))
    state = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
    }))
    city = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
    }))
    district = forms.CharField(max_length=45, required=False, widget=forms.TextInput(attrs={
    }))
    complement = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
    }))


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Nome de Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))


class FormPedido(ModelForm, BaseForm):
    class Meta:
        model = Pedido
        fields = ['status', 'estabelecimento', 'valor_total']


class FormPonto(ModelForm, BaseForm):
    class Meta:
        model = Ponto
        fields = ['cep', 'endereco', 'numero', 'bairro', 'complemento']


PontoFormSet = inlineformset_factory(Pedido, Ponto, form=FormPonto, extra=1)
#
#
# class FormObject(BaseForm):
#     name_item = forms.CharField(widget=forms.TextInput(attrs={'required': True,
#                                                               'maxlength': 100,
#                                                               'placeholder': _('Nome do Objeto')}))
#     description = forms.CharField(widget=forms.Textarea(attrs={'required': False,
#                                                                'maxlength': 300,
#                                                                'placeholder': _('Descricao do Objeto')}))
#     object_type = forms.ChoiceField(choices=object_type, required=True, label=u'Type')
#
#
# class FormObjectView(BaseForm):
#     name_item = forms.CharField(widget=forms.TextInput(attrs={'readonly': True,
#                                                               'maxlength': 100,
#                                                               'placeholder': _('Nome do Objeto')}))
#     description = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 300,
#                                                                'placeholder': _('Descricao do Objeto')}))
#     object_type = forms.ChoiceField(choices=object_type, required=True, label=u'Type')
#
#
# class FormItemUpdate(forms.ModelForm, BaseForm):
#     object_type = forms.ChoiceField(choices=object_type, required=True, label=u'Type')
#
#     class Meta:
#         model = Item
#         fields = ['name_item', 'description']
#
#
# class FormRequirement(forms.ModelForm, BaseForm):
#     class Meta:
#         model = Requirement
#         fields = ['name', 'type', 'description', 'owner']
#         widgets = {'owner': forms.HiddenInput()}
#
#
# class FormDonatorUpdate(forms.ModelForm, FormBaseAddress):
#     cpf = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'maxlength': 150,
#                                                         'placeholder': _('CPF')}))
#     phone = forms.CharField(required=False,
#                             widget=forms.TextInput(attrs={'required': False, 'maxlength': 150,
#                                                           'placeholder': _('Telefone')}))
#     birth_date = forms.CharField(required=False,
#                                  widget=forms.TextInput(attrs={'required': True, 'placeholder': _('Data de Nascimento'),
#                                                                'maxlength': 150}))
#     anonymous = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, required=False, label=u'Type')
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']
#
#     def __init__(self, *args, **kwargs):
#         super(FormDonatorUpdate, self).__init__(*args, **kwargs)
#         self.fields['birth_date'].widget.attrs['class'] += ' datepicker'
#
#
# class FormInstituteUpdate(forms.ModelForm, FormBaseAddress):
#     cnpj = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'maxlength': 200,
#                                                          'placeholder': _('CNPJ')}))
#     phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': False, 'maxlength': 150,
#                                                                           'placeholder': _('Telefone')}))
#     description = forms.CharField(required=False, widget=forms.Textarea(attrs={'maxlength': 300,
#                                                                                'placeholder': _(
#                                                                                    'Descricao da Instituicao')}))
#     site = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': False,
#                                                                          'maxlength': 150,
#                                                                          'placeholder': _('Site')}))
#     social = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': False,
#                                                                            'maxlength': 150,
#                                                                            'placeholder': _('Rede Social')}))
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'email']
#
#     def __init__(self, *args, **kwargs):
#         super(FormInstituteUpdate, self).__init__(*args, **kwargs)
#
#
# class FormAuditView(ModelForm, BaseForm):
#     class Meta:
#         model = Audit
#         fields = ['new_owner', 'donor', 'item', 'is_complete', 'is_deferred']
#
#
# class FormMatchView(ModelForm, BaseForm):
#     class Meta:
#         model = Match
#         fields = ['requirement', 'item', ]
#
#
# class FormOrderView(ModelForm, BaseForm):
#     class Meta:
#         model = Requirement
#         fields = ['name', 'type', 'status', 'owner', 'description', ]
#
#
# class FormDonationView(ModelForm, BaseForm):
#     class Meta:
#         model = Item
#         fields = ['owner', 'description', 'name_item', 'photo', 'status', ]
#
#
# class FormAnonDonation(FormObject):
#     phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': True, 'maxlength': 150,
#                                                                          'placeholder': _('Telefone')}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True, 'maxlength': 150,
#                                                             'placeholder': _('Email')}))
