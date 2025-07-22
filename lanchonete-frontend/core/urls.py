from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ClienteViewSet, PedidoViewSet, 
    LanchoneteViewSet, UsuarioLanchoneteViewSet
)

router = DefaultRouter()
router.register(r'lanchonetes', LanchoneteViewSet, basename='lanchonete')
router.register(r'usuarios-lanchonete', UsuarioLanchoneteViewSet, basename='usuario-lanchonete')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

# API-only URLs with DRF
urlpatterns = [
    path('api/', include(router.urls)),
]