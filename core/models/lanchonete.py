from django.db import models

class Lanchonete(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('inativa', 'Inativa')
    ]

    # Informações básicas
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='lanchonetes/', blank=True, null=True)
    
    # Endereço
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, default='S/N')
    complemento = models.CharField(max_length=255, blank=True, default='')
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=15)
    
    # Entrega
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tempo_estimado = models.PositiveIntegerField(default=30, help_text='Tempo em minutos')
    raio_entrega = models.DecimalField(max_digits=5, decimal_places=1, default=5, help_text='Raio de atendimento em km')
    
    # Funcionamento
    dias_funcionamento = models.CharField(max_length=100, help_text='Dias separados por vírgula', blank=True, null=True, default='')
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)
    
    # Pagamento
    pix = models.BooleanField(default=True)
    chave_pix = models.CharField(max_length=100, blank=True, null=True, default='')
    
    # Status e datas
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativa')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lanchonete'
        verbose_name_plural = 'Lanchonetes'
        ordering = ['nome']

    def __str__(self):
        return self.nome
