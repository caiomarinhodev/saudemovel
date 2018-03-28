# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-23 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_folhapagamento_status_pagamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagamentoMotorista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('valor_total', models.CharField(default='15.00', max_length=50)),
                ('link_pagamento', models.URLField(default='#')),
                ('status_pagamento', models.BooleanField(default=False)),
                ('motorista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Motorista')),
            ],
            options={
                'verbose_name': 'Pagamento de Motoboy',
                'verbose_name_plural': 'Pagamentos de Motoboys',
            },
        ),
        migrations.AlterModelOptions(
            name='folhapagamento',
            options={'verbose_name': 'Pagamento', 'verbose_name_plural': 'Pagamentos'},
        ),
    ]
