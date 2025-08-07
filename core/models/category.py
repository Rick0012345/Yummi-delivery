from django.db import models

                         
class Category(models.Model):
    lanchonete = models.ForeignKey('Lanchonete', on_delete=models.CASCADE, related_name='categorias', null=True, blank=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True, default='')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name