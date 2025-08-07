from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=100, default='')
    telefone = models.CharField(max_length=20, default='')
    endereco = models.CharField(max_length=255, default='')
    numero = models.CharField(max_length=10, default='S/N')
    bairro = models.CharField(max_length=100, default='Centro')
    cidade = models.CharField(max_length=100, default='Não informado')
    estado = models.CharField(max_length=2, default='RJ')
    cep = models.CharField(max_length=15, blank=True, default='')
    complemento = models.CharField(max_length=100, blank=True, default='')
    observacoes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    data_cadastro = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nome

class Category(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=50, unique=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    description = models.TextField(blank=True, null=True, default='')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Optional image field

    def __str__(self):
        return self.name

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo_entrega = models.CharField(max_length=20, choices=[('balcao','Balcão'),('delivery','Delivery'),('mesa','Mesa')], default='balcao')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacao = models.TextField(blank=True, default='')
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey('Pedido', related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    observacao = models.CharField(max_length=255, blank=True, default='')

    def subtotal(self):
        return self.quantidade * self.valor_unitario

class Configuracao(models.Model):
    nome_lanchonete = models.CharField(max_length=100, default='')
    cnpj = models.CharField(max_length=20, default='')
    telefone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    endereco = models.CharField(max_length=255, default='')
    cidade = models.CharField(max_length=100, default='')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tempo_estimado = models.PositiveIntegerField(default=30)
    raio_entrega = models.DecimalField(max_digits=5, decimal_places=1, default=5)
    dias_funcionamento = models.CharField(max_length=100, help_text='Dias separados por vírgula', default='')
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)
    dinheiro = models.BooleanField(default=True)
    cartao_credito = models.BooleanField(default=True)
    cartao_debito = models.BooleanField(default=True)
    pix = models.BooleanField(default=True)
    vale_refeicao = models.BooleanField(default=False)
    chave_pix = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.nome_lanchonete
