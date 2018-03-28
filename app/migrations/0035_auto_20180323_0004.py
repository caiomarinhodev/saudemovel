# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-23 00:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20180322_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolhaPagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('valor_total', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Pagamentos',
                'verbose_name_plural': 'Pagamentos',
            },
        ),
        migrations.CreateModel(
            name='ItemPagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('folha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.FolhaPagamento')),
            ],
            options={
                'verbose_name': 'Item de Pagamento',
                'verbose_name_plural': 'Itens de Pagamento',
            },
        ),
        migrations.AlterModelOptions(
            name='classification',
            options={'verbose_name': 'Avalia\xe7\xe3o Motorista', 'verbose_name_plural': 'Avalia\xe7\xf5es Motorista'},
        ),
        migrations.AlterModelOptions(
            name='configuration',
            options={'verbose_name': 'Configura\xe7\xe3o', 'verbose_name_plural': 'Configura\xe7\xf5es'},
        ),
        migrations.AlterModelOptions(
            name='endereco',
            options={'verbose_name': 'Endere\xe7o de Cliente', 'verbose_name_plural': 'Endere\xe7os de Cliente'},
        ),
        migrations.AlterModelOptions(
            name='pedido',
            options={'verbose_name': 'Rota', 'verbose_name_plural': 'Rotas'},
        ),
        migrations.AlterModelOptions(
            name='ponto',
            options={'verbose_name': 'Ponto de Entrega', 'verbose_name_plural': 'Pontos de Entrega'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'verbose_name': 'Pedido Loja', 'verbose_name_plural': 'Pedidos Loja'},
        ),
        migrations.AddField(
            model_name='itempagamento',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Request'),
        ),
    ]
