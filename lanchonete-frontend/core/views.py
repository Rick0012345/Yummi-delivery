from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from .models import Category, Product, Cliente, Pedido, Configuracao
from .serializers import CategorySerializer, ProductSerializer, ClienteSerializer, PedidoSerializer, ConfiguracaoSerializer

# API viewsets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [IsAuthenticated]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    authentication_classes = [IsAuthenticated]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-data_hora')
    serializer_class = PedidoSerializer
    authentication_classes = [IsAuthenticated]

class ConfiguracaoViewSet(viewsets.ModelViewSet):
    queryset = Configuracao.objects.all()
    serializer_class = ConfiguracaoSerializer
    authentication_classes = [IsAuthenticated]