from django.db import models


class Configuracao(models.Model):
    # Informações básicas
    nome_lanchonete = models.CharField(max_length=100, default='')
    cnpj = models.CharField(max_length=20, default='')
    telefone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    endereco = models.CharField(max_length=255, default='')
    cidade = models.CharField(max_length=100, default='')
    
    # Configurações operacionais
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tempo_estimado = models.PositiveIntegerField(default=30, help_text='Tempo em minutos')
    raio_entrega = models.DecimalField(max_digits=5, decimal_places=1, default=5, help_text='Raio em km')
    
    # Horário de funcionamento
    dias_funcionamento = models.CharField(max_length=100, help_text='Dias separados por vírgula', default='')
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)
    
    # PIX como única forma de pagamento configurável
    chave_pix = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'

    def __str__(self):
        return f'Configuração - {self.nome_lanchonete}'