from django.db import models

class BaseLanchonete(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('inativa', 'Inativa')
    ]

    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativa')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    dias_funcionamento = models.CharField(max_length=100, help_text='Dias separados por vírgula', default='')
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lanchonete'
        verbose_name_plural = 'Lanchonetes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class EnderecoLanchonete(BaseLanchonete):
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, default='S/N')
    complemento = models.CharField(max_length=255, default='')
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=15)


class EntregasLanchonete(BaseLanchonete):
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    raio_entrega = models.DecimalField(max_digits=5, decimal_places=1, default=5, help_text='Raio de atendimento em km')


class PagamentosLanchonete(BaseLanchonete):
    chave_pix = models.CharField(max_length=100, blank=True, default='')
