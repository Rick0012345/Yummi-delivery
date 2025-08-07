from django.contrib import admin
from .models import (
    Cliente, Category, Product, Pedido, PedidoItem, Lanchonete
)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco', 'status', 'data_cadastro')
    search_fields = ('nome', 'telefone', 'endereco')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'status', 'category')
    search_fields = ('name', 'code')
    list_filter = ('status', 'category')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_hora', 'tipo_entrega', 'status', 'total')
    search_fields = ('cliente__nome',)
    list_filter = ('status', 'tipo_entrega')

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'valor_unitario')
    search_fields = ('pedido__id', 'produto__name')



@admin.register(Lanchonete)
class LanchoneteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'cidade', 'status', 'data_criacao')
    search_fields = ('nome', 'cnpj', 'telefone')
    list_filter = ('status', 'cidade', 'estado')