# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-10 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_configuration_has_cozinha'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponto',
            name='is_prepared',
            field=models.BooleanField(default=False),
        ),
    ]