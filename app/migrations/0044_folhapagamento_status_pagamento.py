# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-23 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_folhapagamento_link_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='folhapagamento',
            name='status_pagamento',
            field=models.BooleanField(default=False),
        ),
    ]
