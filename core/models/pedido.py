from django.db import models

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_ENTREGA_CHOICES = [
        ('balcao', 'Balcão'),
        ('entrega', 'Entrega'),
    ]
    lanchonete = models.ForeignKey('Lanchonete', on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo_entrega = models.CharField(max_length=10, choices=TIPO_ENTREGA_CHOICES, default='balcao')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacao = models.TextField(blank=True, default='')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_hora']

    @property
    def taxa_entrega(self):
        """Retorna a taxa de entrega da lanchonete"""
        return self.lanchonete.taxa_entrega if self.lanchonete else 0

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome}'


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    observacao = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def subtotal(self):
        return self.quantidade * self.valor_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.produto.name}'