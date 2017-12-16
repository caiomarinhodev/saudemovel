#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.contrib.auth.models import AnonymousUser
from app.mixins.CustomContextMixin import RedirectMotoristaOcupadoView

from app.forms import FormLogin, FormRegister
from app.models import *

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class LoginView(FormView):
    """
    Displays the login form.
    """
    template_name = 'page/login.html'
    form_class = FormLogin

    def get(self, request, *args, **kwargs):
        try:
            if user and not isinstance(self.request.user, AnonymousUser):
                return redirect(self.get_success_url())
        except:
            return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        print(data)
        user = authenticate(**data)
        print(user)
        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nenhum usuário encontrado')
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        url = '/'
        motorista = None
        loja = None
        try:
            user = self.request.user
        except:
            user = None
        try:
            motorista = user.motorista
        except:
            pass
        
        try:
            loja = user.estabelecimento
        except:
            pass

        if user:
            if loja:
                url = '/app/pedidos/loja'
                loja.is_online = True
                loja.save()
                self.success_url = url
            elif motorista:
                url = '/app/pedidos/motorista'
                motorista.is_online = True
                motorista.save()
                if motorista.ocupado:
                    url = '/app/entregas/motorista'
                self.success_url = url
            elif user.is_superuser:
                url = '/admin'
                self.success_url = url
            else:
                url = '/'
                self.success_url = url
        else:
            url = '/'
            self.success_url = url
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        user = self.request.user
        motorista = None
        loja = None
        try:
            motorista = user.motorista
        except:
            pass
        
        try:
            loja = user.estabelecimento
        except:
            pass
        if motorista:
            motorista.is_online = False
            motorista.save()
        elif loja:
            loja.is_online = False
            loja.save()
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = 'page/register.html'
    form_class = FormRegister
    success_url = '/login'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        aux_obj = User.objects.filter(username=data['username'])
        if len(aux_obj) > 0:
            return self.form_invalid(form)
        user_data = {}
        common_data = {}
        user_data['first_name'] = data['first_name']
        user_data['username'] = data['username']
        user_data['password'] = data['password']
        common_data['endereco'] = data['endereco']
        common_data['phone'] = data['phone']
        common_data['numero'] = data['numero']
        common_data['bairro'] = data['bairro']
        if data['username'] and data['password']:
            new_user = User.objects.create_user(**user_data)
            new_common_user = Estabelecimento(user=new_user, **common_data)
            new_common_user.save()
            messages.success(self.request, 'Novo usuário cadastrado com sucesso.')
        else:
            return self.form_invalid(form)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Não foi possível cadastrar.')
        return super(RegisterView, self).form_invalid(form)

    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError