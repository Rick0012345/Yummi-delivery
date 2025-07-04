from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=15, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')])
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
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
    tipo_entrega = models.CharField(max_length=20, choices=[('balcao','Balcão'),('delivery','Delivery'),('mesa','Mesa')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacao = models.TextField(blank=True)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey('Pedido', related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=7, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True)

    def subtotal(self):
        return self.quantidade * self.valor_unitario

class Configuracao(models.Model):
    nome_lanchonete = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tempo_estimado = models.PositiveIntegerField(default=30)
    raio_entrega = models.DecimalField(max_digits=5, decimal_places=1, default=5)
    dias_funcionamento = models.CharField(max_length=100, help_text='Dias separados por vírgula')
    horario_abertura = models.TimeField()
    horario_fechamento = models.TimeField()
    dinheiro = models.BooleanField(default=True)
    cartao_credito = models.BooleanField(default=True)
    cartao_debito = models.BooleanField(default=True)
    pix = models.BooleanField(default=True)
    vale_refeicao = models.BooleanField(default=False)
    chave_pix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome_lanchonete
