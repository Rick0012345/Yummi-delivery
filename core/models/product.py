from django.db import models
from .category import Category


class Product(models.Model):
    lanchonete = models.ForeignKey('Lanchonete', on_delete=models.CASCADE, related_name='produtos', null=True, blank=True)
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=50, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    description = models.TextField(blank=True, null=True, default='')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        unique_together = ['lanchonete', 'code']  # Código único por lanchonete
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name