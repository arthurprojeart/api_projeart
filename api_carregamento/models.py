from django.db import models


class Romaneio(models.Model):
    ID_Romaneio = models.BigAutoField(primary_key=True)
    Nome_Motorista = models.CharField(max_length=100, blank=True, default='')
    Placa_Carro = models.CharField(max_length=100, blank=True, default='')
    ID_Obra = models.IntegerField(blank=False)
    Data_Inicio = models.DateTimeField(auto_now_add=False, blank=True)
    Usuario_Inicio = models.CharField(max_length=100, blank=True, default='')
    Data_Final = models.DateTimeField(auto_now_add=False, blank=True)
    Usuario_Final = models.CharField(max_length=100, blank=True, default='')
    ID_Status = models.IntegerField(blank=True, default=1)
    class Meta:
        managed = False
        db_table = 'TbRomaneio'

class Pecas(models.Model):
    ID_Peca = models.BigAutoField(primary_key=True)
    #ID_TbRomaneio = models.ForeignKey(Romaneio, on_delete=models.CASCADE)
    ID_TbRomaneio = models.IntegerField(blank=False)
    Usuario = models.CharField(max_length=50,blank=False)
    Ordem_Fabricacao = models.IntegerField(blank=False)
    Nome_Peca = models.CharField(max_length=50,blank=False)
    ID_Obra = models.IntegerField(blank=False)
    Nome_Obra = models.CharField(max_length=50,blank=False)
    ID_Trecho = models.IntegerField(blank=False)
    Nome_Trecho = models.CharField(max_length=50,blank=False)
    Desenho = models.CharField(max_length=10,blank=False)
    Marca = models.CharField(max_length=10,blank=False)
    Peso_Unitario = models.FloatField(blank=False)
    Quantidade_Carregado = models.IntegerField(blank=False)
    Quantidade_Total = models.IntegerField(blank=False)
    Data_Entrada = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'TbPecasRomaneio'
