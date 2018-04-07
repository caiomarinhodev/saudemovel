from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Bairro, Estabelecimento, Pedido, Configuration, Categoria, Request, \
    Produto, Grupo, Opcional, ItemPedido, OpcionalChoice, Endereco, BairroGratis, FormaPagamento


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = ('id', 'nome', 'valor', 'valor_madrugada', 'valor_madrugada_feriado', 'valor_feriado')


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ('tema', 'plano', 'has_cozinha', 'tempo_de_entrega',)


class EstabelecimentoQuickSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer()
    bairro = BairroSerializer()

    class Meta:
        model = Estabelecimento
        fields = ('id', 'user', 'configuration', 'phone', 'photo', 'is_online', 'cnpj', 'full_address', 'is_approved',
                  'bairro', 'endereco', 'numero', 'complemento', 'lat', 'lng',)


class CategoriaQuickSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()

    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'estabelecimento')


class ProdutoQuickSerializer(serializers.ModelSerializer):
    categoria = CategoriaQuickSerializer()

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'categoria', 'preco_base', 'disponivel')


class GrupoQuickSerializer(serializers.ModelSerializer):
    produto = ProdutoQuickSerializer()

    class Meta:
        model = Grupo
        fields = ('id', 'identificador', 'titulo', 'limitador', 'produto', 'obrigatoriedade', 'tipo', 'disponivel')


class OpcionalFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcional
        fields = ('id', 'nome', 'descricao', 'grupo', 'valor', 'disponivel',)


class GrupoFullSerializer(serializers.ModelSerializer):
    opcional_set = OpcionalFullSerializer(many=True, read_only=True)

    class Meta:
        model = Grupo
        fields = ('id', 'identificador', 'titulo', 'limitador', 'obrigatoriedade', 'tipo', 'disponivel',
                  'opcional_set')


class ProdutoFullSerializer(serializers.ModelSerializer):
    grupo_set = GrupoFullSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco_base', 'disponivel', 'grupo_set')


class CategoriaFullSerializer(serializers.ModelSerializer):
    produto_set = ProdutoFullSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'produto_set',)


class BairroGratisSerializer(serializers.ModelSerializer):
    bairro = BairroSerializer()

    class Meta:
        model = BairroGratis
        fields = ('id', 'bairro',)


class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = ('id', 'forma', 'cartao')


class EstabelecimentoFullSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer()
    bairro = BairroSerializer()
    user = UserSerializer()
    categoria_set = CategoriaFullSerializer(many=True, read_only=True)
    bairrogratis_set = BairroGratisSerializer(many=True, read_only=True)
    formapagamento_set = FormaPagamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Estabelecimento
        fields = ('id', 'user', 'configuration', 'phone', 'photo', 'is_online', 'cnpj', 'full_address', 'is_approved',
                  'bairro', 'endereco', 'numero', 'complemento', 'lat', 'lng', 'categoria_set', 'bairrogratis_set',
                  'formapagamento_set'
                  )


class PedidoSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()
    motorista = UserSerializer()

    class Meta:
        model = Pedido
        fields = ('id',
                  'status', 'estabelecimento', 'coletado', 'is_complete', 'status_cozinha', 'valor_total',
                  'btn_finalizado',
                  'is_draft', 'motorista', 'duration', 'distance')


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'id',
            'cliente',
            'estabelecimento',
            'status_pedido',
            'subtotal',
            'valor_total',
            'troco',
            'resultado_troco',
            'forma_pagamento',
            'endereco_entrega',
            'pedido'
        )


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ('id', 'pedido', 'produto', 'observacoes')


class OpcionalChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionalChoice
        fields = ('id', 'opcional', 'item_pedido',)


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'cliente', 'endereco_completo', 'valor_entrega', 'endereco', 'numero', 'bairro', 'complemento')
