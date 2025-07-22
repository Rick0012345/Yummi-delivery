from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Category, Product, Cliente, Pedido, Lanchonete, UsuarioLanchonete
from .serializers import (
    CategorySerializer, ProductSerializer, ClienteSerializer, 
    PedidoSerializer, LanchoneteSerializer, UsuarioLanchoneteSerializer
)

# Mixin para filtrar por lanchonete
class LanchoneteFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        lanchonete_id = self.request.session.get('lanchonete_ativa')
        if lanchonete_id:
            return queryset.filter(lanchonete_id=lanchonete_id)
        return queryset.none()
    
    def perform_create(self, serializer):
        lanchonete_id = self.request.session.get('lanchonete_ativa')
        if lanchonete_id:
            lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id)
            serializer.save(lanchonete=lanchonete)

# API viewsets
class LanchoneteViewSet(viewsets.ModelViewSet):
    serializer_class = LanchoneteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas lanchonetes do usuário logado
        return Lanchonete.objects.filter(
            Q(proprietario=self.request.user) |
            Q(usuariolanchonete__usuario=self.request.user, usuariolanchonete__ativo=True)
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(proprietario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def selecionar(self, request, pk=None):
        """Seleciona uma lanchonete como ativa na sessão"""
        lanchonete = self.get_object()
        request.session['lanchonete_ativa'] = lanchonete.id
        request.session['lanchonete_nome'] = lanchonete.nome
        return Response({'message': f'Lanchonete {lanchonete.nome} selecionada com sucesso'})

class UsuarioLanchoneteViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioLanchoneteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Retorna apenas vínculos das lanchonetes do usuário
        return UsuarioLanchonete.objects.filter(
            lanchonete__proprietario=self.request.user
        )

class CategoryViewSet(LanchoneteFilterMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(LanchoneteFilterMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ClienteViewSet(LanchoneteFilterMixin, viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class PedidoViewSet(LanchoneteFilterMixin, viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-data_hora')
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]