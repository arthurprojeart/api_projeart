from django.db import models


class Romaneio(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Usuario = models.CharField(max_length=100, blank=True, default='')
    Nome_Motorista = models.CharField(max_length=100, blank=True, default='')
    Placa_Carro = models.CharField(max_length=100, blank=True, default='')
    Data_Inicio = models.DateTimeField(auto_now_add=False, blank=True)
    Data_Final = models.DateTimeField(auto_now_add=False, blank=True)
    ID_Status = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        managed = False
        db_table = 'TbRomaneio'

class Pecas(models.Model):
    ID = models.BigAutoField(primary_key=True)
    id_romaneio = models.IntegerField(blank=False)
    id_peca = models.IntegerField(blank=False)
    qtd_peca = models.IntegerField(blank=False)
    usuario = models.CharField(max_length=25,blank=False)
    data_carregamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TbRomaneioPecas'
