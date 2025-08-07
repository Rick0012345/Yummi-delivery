from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    lanchonete = models.ForeignKey('Lanchonete', on_delete=models.CASCADE, related_name='clientes', null=True, blank=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, default='S/N')
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=15, blank=True, default='')
    complemento = models.CharField(max_length=255, blank=True, default='')
    observacoes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    data_cadastro = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome