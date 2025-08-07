from rest_framework import serializers
from .models import Category, Product, Cliente, Pedido, PedidoItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoItem
        fields = ['produto', 'quantidade', 'valor_unitario', 'observacao']

class PedidoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True)
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'data_hora', 'tipo_entrega', 'status', 'observacao', 'taxa_entrega', 'total', 'itens']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            PedidoItem.objects.create(pedido=pedido, **item_data)
        return pedido