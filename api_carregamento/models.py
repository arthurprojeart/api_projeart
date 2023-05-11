from django.db import models



class Romaneio(models.Model):
    romaneio_id = models.BigAutoField(primary_key=True)
    #peca_id = models.ForeignKey(Pecas, on_delete=models.CASCADE, db_column='peca_id')
    #peca_id = models.IntegerField(blank=True)
    Nome_Motorista = models.CharField(max_length=100, blank=True, default='')
    Placa_Carro = models.CharField(max_length=100, blank=True, default='')
    ID_Obra = models.IntegerField(blank=True)
    Data_Inicio = models.DateTimeField(auto_now_add=False, blank=True)
    Usuario_Inicio = models.CharField(max_length=100, blank=True, default='')
    Data_Final = models.DateTimeField(auto_now_add=False, blank=True)
    Usuario_Final = models.CharField(max_length=100, blank=True, default='')
    ID_Status = models.CharField(max_length=20, blank=True, default='')

    # Pecas = models.IntegerField(blank=True, default=1)
    class Meta:
        managed = False
        db_table = 'TbRomaneio'

class Pecas(models.Model):
    leitura_id = models.BigAutoField(primary_key=True)
    romaneio_id = models.ForeignKey(Romaneio, on_delete=models.CASCADE,db_column='romaneio_id', related_name='pecas_romaneio')
    #romaneio_id = models.IntegerField(blank=False)
    Usuario = models.CharField(max_length=50,blank=False)
    Ordem_Fabricacao = models.IntegerField(blank=False)
    Nome_Peca = models.CharField(max_length=200,blank=False)
    ID_Obra = models.IntegerField(blank=False)
    Nome_Obra = models.CharField(max_length=200,blank=False)
    ID_Trecho = models.IntegerField(blank=False)
    Nome_Trecho = models.CharField(max_length=200,blank=False)
    Desenho = models.CharField(max_length=10,blank=False)
    Marca = models.CharField(max_length=10,blank=False)
    Peso_Unitario = models.FloatField(blank=False)
    Quantidade_Carregado = models.IntegerField(blank=False)
    Quantidade_Total = models.IntegerField(blank=False)
    Data_Entrada = models.DateTimeField(auto_now_add=True)
    Quantidade_Recebida = models.IntegerField(blank=False)
    Usuario_Recebimento = models.CharField(max_length=50,blank=False)
    Data_Recebida = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TbPecasRomaneio'


