# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-26 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_configuration_has_loja_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='blocked_cozinha',
            field=models.BooleanField(default=False),
        ),
    ]
