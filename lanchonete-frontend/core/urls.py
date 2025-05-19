from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'clientes', views.ClienteViewSet, basename='cliente')

# API-only URLs with DRF
urlpatterns = [
    path('api/', include(router.urls)),
]