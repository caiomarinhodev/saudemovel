#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.contrib.auth.models import AnonymousUser

from app.forms import FormLogin

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class LoginView(FormView):
    """
    Displays the login form.
    """
    template_name = 'page/login.html'
    form_class = FormLogin

    def get(self, request, *args, **kwargs):
        if not isinstance(self.request.user, AnonymousUser):
            return redirect(self.get_success_url())
        else:
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

        if user:
            if loja:
                url = '/app/pedidos/loja'
                self.success_url = url
            elif motorista:
                url = '/app/pedidos/motorista'
                self.success_url = url
            else:
                url = '/admin'
                self.success_url = url
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)
