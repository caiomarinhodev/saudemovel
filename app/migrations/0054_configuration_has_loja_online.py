# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-26 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_opcional_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='has_loja_online',
            field=models.BooleanField(default=False),
        ),
    ]
