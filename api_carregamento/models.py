from django.db import models


class Romaneio(models.Model):
    ID = models.BigAutoField(primary_key=True)

    Nome_Motorista = models.CharField(max_length=100, blank=True, default='')
    Placa_Carro = models.CharField(max_length=100, blank=True, default='')
    ID_Obra = models.IntegerField(blank=False)
    Usuario_Inicio = models.CharField(max_length=100, blank=True, default='')
    Data_Inicio = models.DateTimeField(auto_now_add=False, blank=True)
    Usuario_Final = models.CharField(max_length=100, blank=True, default='')
    Data_Final = models.DateTimeField(auto_now_add=False, blank=True)
    ID_Status = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        managed = False
        db_table = 'TbRomaneio'

class Pecas(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Usuario = models.CharField(max_length=50,blank=False)
    ID_TbRomaneio = models.IntegerField(blank=True)
    Ordem_Fabricacao = models.IntegerField(blank=False)
    Nome_Peca = models.CharField(max_length=50,blank=False)
    ID_Obra = models.IntegerField(blank=False)
    Nome_Obra = models.CharField(max_length=50,blank=False)
    ID_Trecho = models.IntegerField(blank=False)
    Nome_Trecho = models.CharField(max_length=50,blank=False)
    Quantidade_Carregado = models.IntegerField(blank=False)
    Data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'TbPecasRomaneio'
