# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-23 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_folhapagamento_estabelecimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='folhapagamento',
            name='valor_cobrar',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
