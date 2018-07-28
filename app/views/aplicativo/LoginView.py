#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.views.generic import RedirectView

from app.forms import FormLogin

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class LoginView(FormView):
    """
    Displays the login form.
    """
    template_name = 'app_template/login.html'
    form_class = FormLogin
    success_url = '/aplicativo/consulta/'

    def form_valid(self, form):
        data = form.cleaned_data
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


class LogoutAppView(RedirectView):
    url = '/aplicativo/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutAppView, self).get(request, *args, **kwargs)
