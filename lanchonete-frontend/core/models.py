from django.db import models

# Modelos simplificados apenas para o frontend
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    
    def __str__(self):
        return self.nome

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    observacao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
