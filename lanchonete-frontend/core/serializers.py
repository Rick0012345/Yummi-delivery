from rest_framework import serializers
from .models import Category, Product, Cliente, Pedido, PedidoItem, Lanchonete, UsuarioLanchonete

class LanchoneteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lanchonete
        fields = '__all__'
        read_only_fields = ['proprietario', 'data_cadastro']

class UsuarioLanchoneteSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    lanchonete_nome = serializers.CharField(source='lanchonete.nome', read_only=True)
    
    class Meta:
        model = UsuarioLanchonete
        fields = ['id', 'usuario', 'usuario_nome', 'lanchonete', 'lanchonete_nome', 'tipo', 'ativo', 'data_vinculacao']
        read_only_fields = ['data_vinculacao']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['lanchonete']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['lanchonete']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['lanchonete']

class PedidoItemSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.name', read_only=True)
    
    class Meta:
        model = PedidoItem
        fields = ['produto', 'produto_nome', 'quantidade', 'valor_unitario', 'observacao']

class PedidoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'lanchonete', 'cliente', 'cliente_nome', 'data_hora', 'tipo_entrega', 'status', 'observacao', 'taxa_entrega', 'total', 'itens']
        read_only_fields = ['lanchonete']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens', [])
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            PedidoItem.objects.create(pedido=pedido, **item_data)
        return pedido