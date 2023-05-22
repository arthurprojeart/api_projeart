from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api_carregamento.models import Romaneio, Pecas, Ordens, LeiturasCarregamento, LeiturasRecebimento#Carregamento, 
from django.db.models import Sum        
from django.db.models import F

class RomaneioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Romaneio
        #owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['romaneio_id',
                  'Nome_Motorista',
                  'Placa_Carro', 
                  'ID_Obra',
                  'Data_Inicio', 
                  'Usuario_Inicio',
                  'Data_Final',
                  'Usuario_Final',
                  'ID_Status']
        read_only_fields = ['ID', 'Data_Final']

class RomaneioAtualizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Romaneio
        #owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['romaneio_id',
                  'Data_Final',
                  'Usuario_Final',
                  'ID_Status'
                  ]
        read_only_fields = ['ID', 
                            'ID_Obra',
                            'Data_Inicio', 
                            'Usuario_Inicio', 
                            'Nome_Motorista',
                            'Placa_Carro'
                            'Nome_Motorista',
                            'Placa_Carro', 
                            'ID_Obra',
                            'Data_Inicio', 
                            'Usuario_Inicio',
                            ]

class PecasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pecas
        fields = [
                  'leitura_id', 
                  'romaneio_id', 
                  'Usuario',
                  'Ordem_Fabricacao',
                  'Nome_Peca',
                  'ID_Obra', 
                  'Nome_Obra', 
                  'ID_Trecho',
                  'Nome_Trecho',
                  'Desenho',
                  'Marca',
                  'Peso_Unitario',
                  'Quantidade_Carregado',
                  #'Quantidade_Disponivel',
                  'Quantidade_Total',
                  'Data_Entrada',
                  ]
        read_only_fields = ['ID']

class RecebimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pecas
        fields = [
                    'Ordem_Fabricacao',
                    'romaneio_id', 
                    'Quantidade_Recebida',
                    'Data_Recebida',
                    'Usuario_Recebimento',
                  ]
        read_only_fields = ['ID', 
                            'leitura_id', 
                            'Nome_Peca', 
                            'ID_Obra', 
                            'Nome_Obra', 
                            'ID_Trecho',
                            'Nome_Trecho',
                            'Desenho',
                            'Marca',
                            'Peso_Unitario',
                            'Quantidade_Carregado',
                            'Quantidade_Disponivel',
                            'Quantidade_Total',
                            'Data_Entrada',
                            ]

class PecasTrechoSerializer(serializers.Serializer):
    romaneio_id = serializers.IntegerField()
    ID_Trecho = serializers.IntegerField()
    Nome_Trecho = serializers.CharField()
    Quantidade_Trecho = serializers.DecimalField(max_digits=10, decimal_places=2)
    Peso_Trecho = serializers.DecimalField(max_digits=10, decimal_places=2)

from django.db.models import Prefetch

class RomaneioTrechosSerializer(serializers.ModelSerializer):
    Trechos_Romaneio = serializers.SerializerMethodField()

    class Meta:
        model = Romaneio
        fields = '__all__'
        read_only_fields = ['ID']
    
    def get_Trechos_Romaneio(self, obj):

        ordens = LeiturasCarregamento.objects.filter(romaneio_id=obj.romaneio_id).select_related('Ordem_Fabricacao').values(
            'romaneio_id', 'Ordem_Fabricacao__ID_Trecho', 'Ordem_Fabricacao__Nome_Trecho',
        ).annotate(
            Quantidade_Trecho= Sum('Quantidade_Carregada'),
            Peso_Trecho = Sum(F('Quantidade_Carregada')*F('Ordem_Fabricacao__Peso_Unitario')),
            ID_Trecho = F('Ordem_Fabricacao__ID_Trecho'),
            Nome_Trecho = F('Ordem_Fabricacao__Nome_Trecho'),
        ).order_by()

        serializer = PecasTrechoSerializer(ordens, many=True)
        return serializer.data
   
class LeituraSerializer(serializers.Serializer):
    #romaneio_id = serializers.IntegerField()
    Leitura_ID = serializers.IntegerField()
    Usuario = serializers.CharField()
    Ordem_Fabricacao = serializers.IntegerField()
    Quantidade_Carregada = serializers.DecimalField(max_digits=10, decimal_places=2)
    Data_Carregamento = serializers.DateTimeField()

class PecasTesteSerializer(serializers.Serializer):

    #leitura_id = serializers.IntegerField()
    romaneio_id = serializers.IntegerField()
    #Usuario = serializers.CharField()
    Ordem_Fabricacao = serializers.IntegerField()
    Nome_Peca = serializers.CharField()
    ID_Obra = serializers.IntegerField()
    Nome_Obra = serializers.CharField()
    ID_Trecho = serializers.IntegerField()
    Nome_Trecho = serializers.CharField()
    Desenho = serializers.CharField()
    Marca = serializers.CharField()
    Peso_Unitario = serializers.FloatField()
    quantidade_total = serializers.IntegerField()
    # Quantidade_Carregado = serializers.IntegerField()
    # Quantidade_Total = serializers.IntegerField()
    # Data_Entrada = serializers.DateTimeField()

class PecasLeiturasSerializer(serializers.ModelSerializer):
    leituras_romaneio = serializers.SerializerMethodField()
    quantidade_total = serializers.IntegerField()
    romaneio_id = serializers.IntegerField(read_only=True)
    #quantidade_projeto = serializers.SerializerMethodField()

    class Meta:
        model = Pecas
        # fields = '__all__'
        fields = [
                  'romaneio_id', 
                  'Ordem_Fabricacao',
                  'Nome_Peca',
                  'ID_Obra', 
                  'Nome_Obra', 
                  'ID_Trecho',
                  'Nome_Trecho',
                  'Desenho',
                  'Marca',
                  'Peso_Unitario',
                  'quantidade_total',
                  'leituras_romaneio',
                  ]
        read_only_fields = [
                            'ID',
                            'Usuario',
                            #'romaneio_id',
                            'leitura_id', 
                            'Data_Entrada',
                            'Quantidade_Total',
                            'Quantidade_Carregado',
                            'Usuario_Recebimento',
                            'Quantidade_Recebida'
                            ]
    def get_leituras_romaneio(self, obj):

        queryset = Pecas.objects.filter(Ordem_Fabricacao = obj['Ordem_Fabricacao'], romaneio_id=obj['romaneio_id']).values(
            'leitura_id', 'Ordem_Fabricacao', 'Quantidade_Carregado', 'Usuario', 'Data_Entrada'
        ).annotate(
            quantidade_total= Sum('Quantidade_Carregado'),
            peso_total = Sum(F('Quantidade_Carregado')*F('Peso_Unitario'))
        ).order_by()
        serializer = LeituraSerializer(queryset, many=True)
        return serializer.data
    
    def get_quantidade_projeto(self,obj):
        return obj.Quantidade_Total

class PecasRecebimentoSerializer(serializers.ModelSerializer):
    pecas_romaneio = serializers.SerializerMethodField()
    trechos_romaneio = serializers.SerializerMethodField()
    # leituras_romaneio = PecasLeiturasSerializer(many=True, read_only=True)
    # leituras_romaneio = serializers.SerializerMethodField()
    # pecas_romaneio = PecasLeiturasSerializer(many=True)#, read_only=True)
    #Ordem_Fabricacao = PecasSerializer()
    class Meta:
        model = Romaneio
        fields = ['romaneio_id',
                  'pecas_romaneio',
                #   'leituras_romaneio',
                  'Nome_Motorista',
                  'Placa_Carro', 
                  'ID_Obra',
                  'trechos_romaneio',
                  'Data_Inicio', 
                  'Usuario_Inicio',
                  'Data_Final',
                  'Usuario_Final',
                  'ID_Status']
        read_only_fields = ['ID', 'Data_Final']
    
    # def create(self, validated_data):
    #         leituras_romaneio = validated_data.pop('leituras_romaneio')
    #         pecas_instancia = Pecas.objects.create(**validated_data)
    #         for peca in leituras_romaneio:
    #             Pecas.objects.create(user=pecas_instancia,**peca)
    #         return pecas_instancia

    def get_trechos_romaneio(self, obj):
        queryset = Pecas.objects.filter(romaneio_id=obj.romaneio_id).values(
            'romaneio_id', 'ID_Trecho', 'Nome_Trecho',
        ).annotate(
            quantidade_total= Sum('Quantidade_Carregado'),
            peso_total = Sum(F('Quantidade_Carregado')*F('Peso_Unitario'))
        ).order_by()
        # print(queryset)
        serializer = PecasTrechoSerializer(queryset, many=True)
        return serializer.data
    
    def get_pecas_romaneio(self, obj):

        queryset_pecas = Pecas.objects.filter(romaneio_id=obj.romaneio_id).values(
                'romaneio_id', 
                'Ordem_Fabricacao',
                'Nome_Peca',
                'ID_Obra', 
                'Nome_Obra', 
                'ID_Trecho',
                'Nome_Trecho',
                'Desenho',
                'Marca',
                'Peso_Unitario',

                #'quantidade_total',
        ).annotate(
            quantidade_total= Sum('Quantidade_Carregado'),
            
        ).order_by()


        queryset_leituras = Pecas.objects.filter(romaneio_id=obj.romaneio_id).values(
            'leitura_id', 'Ordem_Fabricacao', 'Quantidade_Carregado', 'Usuario', 'Data_Entrada'
        ).annotate(
            quantidade_total= Sum('Quantidade_Carregado'),
            peso_total = Sum(F('Quantidade_Carregado')*F('Peso_Unitario'))
        ).order_by()
        
        serializer_leitura = LeituraSerializer(queryset_leituras, many=True)
        serializer_pecas = PecasTesteSerializer(queryset_pecas, many=True)

        dict_pecas = dict(serializer_pecas.data[0])
        ## Fazer um for para iterar apenas os registros de uma ordem especial
        dict_pecas['leituras_romaneio'] = serializer_leitura.data

        return dict_pecas

class OrdensSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ordens
        fields = [
                  'Ordem_Fabricacao',
                  'romaneio_id', 
                  'Usuario',
                  'Nome_Peca',
                  'ID_Obra', 
                  'Nome_Obra', 
                  'ID_Trecho',
                  'Nome_Trecho',
                  'Desenho',
                  'Marca',
                  'Peso_Unitario',
                  'Quantidade_Produzida',
                  'Quantidade_Projeto'
                  ]
        read_only_fields = ['ID']

class LeiturasCarregamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeiturasCarregamento
        fields = [
                #   'Leitura_ID',
                  'Ordem_Fabricacao', 
                  'romaneio_id',
                  'Usuario',
                  'Quantidade_Carregada', 
                  'Data_Carregamento', 
                  ]
        read_only_fields = ['Leitura_ID']

class PecasLeiturasCarregamentoSerializer(serializers.ModelSerializer):
    Leituras_Carregamento = serializers.SerializerMethodField()
    Quantidade_Total = serializers.SerializerMethodField()

    class Meta:
        model = Ordens
        fields = '__all__'

    def get_Leituras_Carregamento(self, obj):
        queryset = LeiturasCarregamento.objects.filter(Ordem_Fabricacao = obj.Ordem_Fabricacao, romaneio_id=obj.romaneio_id)
        serializer = LeituraSerializer(queryset, many=True)
        return serializer.data
    
    def get_Quantidade_Total(self,obj):
        queryset = LeiturasCarregamento.objects.filter(Ordem_Fabricacao = obj.Ordem_Fabricacao)
        Quantidade_Total = sum([valor.Quantidade_Carregada for valor in queryset])
        return Quantidade_Total

class LeituraRecebimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeiturasRecebimento
        fields = '__all__'
        read_only_fields = ['Leitura_ID', 'Data_Recebimento']

class PecasLeiturasRecebimentoSerializer(serializers.ModelSerializer):
    Leituras_Recebimento = serializers.SerializerMethodField()
    Trechos_Romaneio = serializers.SerializerMethodField()

    class Meta:
        model = Romaneio
        fields = '__all__'
        # fields = ['romaneio_id',
        #         #   'Leituras_Recebimento',
        #           'Trechos_Romaneio',
        #           'Nome_Motorista',
        #           'Placa_Carro', 
        #           'ID_Obra',
        #           'Trechos_Romaneio',
        #           'Data_Inicio', 
        #           'Usuario_Inicio',
        #           'Data_Final',
        #           'Usuario_Final',
        #           'ID_Status']
        read_only_fields = ['ID', 'Data_Final']
    
    # def get_Trechos_Romaneio(self, obj):

    #     ordens = Ordens.objects.all().prefetch_related('Leituras_Recebimento').values(
    #         'romaneio_id', 'ID_Trecho', 'Nome_Trecho',
    #     ).annotate(
    #         Qantidade_Trecho= Sum('Quantidade_Recebida'),
    #         Peso_Trecho = Sum(F('Quantidade_Recebida')*F('Peso_Unitario'))
    #     ).order_by()

    #     for ordem in ordens:
    #         leituras = ordem.Leituras_Recebimento.all()
    #     serializer = PecasTrechoSerializer(leituras, many=True)
    #     return serializer.data
    
    def get_Trechos_Romaneio(self, obj):
        ordens = LeiturasCarregamento.objects.filter(romaneio_id=obj.romaneio_id).select_related('Ordem_Fabricacao').values(
            'romaneio_id', 'Ordem_Fabricacao__ID_Trecho', 'Ordem_Fabricacao__Nome_Trecho',
            ).annotate(
                Quantidade_Trecho= Sum('Quantidade_Carregada'),
                Peso_Trecho = Sum(F('Quantidade_Carregada')*F('Ordem_Fabricacao__Peso_Unitario')),
                ID_Trecho = F('Ordem_Fabricacao__ID_Trecho'),
                Nome_Trecho = F('Ordem_Fabricacao__Nome_Trecho'),
            ).order_by()
        serializer = PecasTrechoSerializer(ordens, many=True)
        return serializer.data

    def get_Leituras_Carregamento(self, obj):
        queryset = LeiturasCarregamento.objects.filter(Ordem_Fabricacao = obj.Ordem_Fabricacao, romaneio_id=obj.romaneio_id)
        serializer = LeituraSerializer(queryset, many=True)
        return serializer.data
    
    