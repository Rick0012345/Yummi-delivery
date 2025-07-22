from django.contrib import admin
from .models import (
    Cliente, Category, Product, Pedido, PedidoItem, Lanchonete, UsuarioLanchonete
)

@admin.register(Lanchonete)
class LanchoneteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'cidade', 'proprietario', 'ativa', 'data_cadastro')
    list_filter = ('ativa', 'cidade', 'estado')
    search_fields = ('nome', 'cnpj', 'proprietario__username')
    readonly_fields = ('data_cadastro',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'telefone', 'email', 'proprietario', 'ativa')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'bairro', 'cidade', 'estado', 'cep')
        }),
        ('Configurações Operacionais', {
            'fields': ('taxa_entrega', 'tempo_estimado', 'raio_entrega', 'dias_funcionamento', 'horario_abertura', 'horario_fechamento')
        }),
        ('Formas de Pagamento', {
            'fields': ('dinheiro', 'cartao_credito', 'cartao_debito', 'pix', 'vale_refeicao', 'chave_pix')
        }),
        ('Outros', {
            'fields': ('logo', 'data_cadastro')
        }),
    )

@admin.register(UsuarioLanchonete)
class UsuarioLanchoneteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'lanchonete', 'tipo', 'ativo', 'data_vinculacao')
    list_filter = ('tipo', 'ativo', 'lanchonete')
    search_fields = ('usuario__username', 'lanchonete__nome')
    readonly_fields = ('data_vinculacao',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco', 'lanchonete', 'status', 'data_cadastro')
    list_filter = ('status', 'lanchonete')
    search_fields = ('nome', 'telefone', 'endereco')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'lanchonete', 'description')
    list_filter = ('lanchonete',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'status', 'category', 'lanchonete')
    list_filter = ('status', 'category', 'lanchonete')
    search_fields = ('name', 'code')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'lanchonete', 'data_hora', 'tipo_entrega', 'status', 'total')
    list_filter = ('status', 'tipo_entrega', 'lanchonete')
    search_fields = ('cliente__nome',)

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'valor_unitario')
    search_fields = ('pedido__id', 'produto__name')