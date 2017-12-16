#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.contrib.auth.models import User

from app.models import Notification, Location, Motorista
from app.views.snippet_template import render_block_to_string


from django.http import JsonResponse

@require_http_methods(["GET"])
def send_position_motorista(request, lat, lng):
    loc = Location(user=request.user, lat=lat, lng=lng)
    loc.save()
    return HttpResponse('')


@require_http_methods(["GET"])
def get_position_motorista(request, pk_user):
    user = User.objects.get(id=pk_user)
    pto = user.location_set.last()
    if pto:
        return JsonResponse({'lat':pto.lat, 'lng':pto.lng})
    else:
        return JsonResponse({'lat':'', 'lng':''})
