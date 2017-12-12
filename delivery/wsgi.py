"""wsgi.py: Arquivo de configuracao de comunicacao com o servidor."""
import os

from django.core.wsgi import get_wsgi_application

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"

"""
WSGI config for default project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery.settings")

application = get_wsgi_application()

from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(application)
