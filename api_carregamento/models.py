from django.db import models

class Carregamento(models.Model):
    owner = models.ForeignKey('auth.User', related_name='api_carregamento', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=100, blank=True, default='')
    carregamento = models.CharField(max_length=100, blank=True, default='')
    pecas = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['data']
