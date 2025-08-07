from django.db import models


class Lanchonete(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('inativa', 'Inativa')
    ]
    
    # Informações básicas
    nome = models.CharField(max_length=100, default='')
    cnpj = models.CharField(max_length=20, default='', unique=True)
    telefone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    
    # Endereço
    endereco = models.CharField(max_length=255, default='')
    numero = models.CharField(max_length=10, default='S/N')
    bairro = models.CharField(max_length=100, default='Centro')
    cidade = models.CharField(max_length=100, default='')
    estado = models.CharField(max_length=2, default='RJ')
    cep = models.CharField(max_length=15, blank=True, default='')
    
    # Configurações operacionais
    logo = models.ImageField(upload_to='lanchonetes/logos/', blank=True, null=True)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tempo_estimado = models.PositiveIntegerField(default=30, help_text='Tempo em minutos')
    raio_entrega = models.DecimalField(max_digits=5, decimal_places=1, default=5, help_text='Raio em km')
    
    # Horário de funcionamento
    dias_funcionamento = models.CharField(max_length=100, help_text='Dias separados por vírgula', default='')
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)
    
    # Formas de pagamento
    pix = models.BooleanField(default=True)
    chave_pix = models.CharField(max_length=100, blank=True, default='')
    
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