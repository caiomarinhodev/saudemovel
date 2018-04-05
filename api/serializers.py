from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Bairro, Estabelecimento, Pedido, Ponto, Configuration, Categoria, FolhaPagamento, Request, \
    Avaliacao, BairroGratis, Chamado, Produto, Grupo, Opcional


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = ('nome', 'valor', 'valor_madrugada', 'valor_madrugada_feriado', 'valor_feriado')


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ('tema', 'plano', 'has_cozinha', 'tempo_de_entrega',)


class EstabelecimentoQuickSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer()
    bairro = BairroSerializer()

    class Meta:
        model = Estabelecimento
        fields = ('user', 'configuration', 'phone', 'photo', 'is_online', 'cnpj', 'full_address', 'is_approved',
                  'bairro', 'endereco', 'numero', 'complemento', 'lat', 'lng',)


class GrupoQuickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ('id', 'identificador', 'titulo', 'limitador', 'obrigatoriedade', 'tipo', 'disponivel')


class ProdutoQuickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco_base', 'disponivel')


class CategoriaQuickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nome',)


class OpcionalFullSerializer(serializers.ModelSerializer):
    grupo_set = GrupoQuickSerializer(many=True, read_only=True)

    class Meta:
        model = Opcional
        fields = ('id', 'nome', 'descricao', 'grupo', 'valor', 'disponivel', 'grupo_set')


class GrupoFullSerializer(serializers.ModelSerializer):
    produto = ProdutoQuickSerializer()
    opcional_set = OpcionalFullSerializer(many=True, read_only=True)

    class Meta:
        model = Grupo
        fields = ('id', 'identificador', 'titulo', 'limitador', 'obrigatoriedade', 'tipo', 'disponivel', 'produto',
                  'opcional_set')


class ProdutoFullSerializer(serializers.ModelSerializer):
    categoria = CategoriaQuickSerializer()
    grupo_set = GrupoFullSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco_base', 'categoria', 'disponivel', 'grupo_set')


class CategoriaFullSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()
    produto_set = ProdutoFullSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'estabelecimento', 'produto_set',)


class EstabelecimentoFullSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer()
    bairro = BairroSerializer()
    user = UserSerializer()
    categoria_set = CategoriaFullSerializer(many=True, read_only=True)
    pedido_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    ponto_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    formapagamento_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    request_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    avaliacao_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    folhapagamento_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    bairrogratis_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    chamado_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Estabelecimento
        fields = ('id', 'user', 'configuration', 'phone', 'photo', 'is_online', 'cnpj', 'full_address', 'is_approved',
                  'bairro', 'endereco', 'numero', 'complemento', 'lat', 'lng', 'pedido_set', 'ponto_set',
                  'categoria_set', 'formapagamento_set', 'request_set', 'avaliacao_set', 'folhapagamento_set',
                  'bairrogratis_set', 'chamado_set')


class PedidoSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()
    motorista = UserSerializer()

    class Meta:
        model = Pedido
        fields = (
            'status', 'estabelecimento', 'coletado', 'is_complete', 'status_cozinha', 'valor_total', 'btn_finalizado',
            'is_draft', 'motorista', 'duration', 'distance')


class PontoSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()
    pedido = PedidoSerializer()

    class Meta:
        model = Ponto
        fields = ('cliente', 'telefone', 'observacoes', 'estabelecimento', 'pedido', 'full_address', 'status',
                  'duration', 'distance', 'itens', 'is_prepared')
