from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api_carregamento.models import Romaneio, Pecas#Carregamento, 


# class UserSerializer(serializers.ModelSerializer):
#     carregamento = serializers.PrimaryKeyRelatedField(many=True, queryset=Carregamento.objects.all())

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'carregamento']

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

# class CarregamentoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Carregamento
#         owner = serializers.ReadOnlyField(source='owner.username')
#         fields = ['id', 'owner','nome', 'carregamento', 'pecas']

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
                            'Data_Final',
                            'Usuario_Final',
                            'ID_Status']


# class PecasSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pecas
#         fields = '__all__'

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
                            'Quantidade_Total',
                            'Data_Entrada',
                            ]

class PecasRecebimentoSerializer(serializers.ModelSerializer):
    pecas_romaneio = PecasSerializer(many=True)# many=True,
    #Ordem_Fabricacao = PecasSerializer()
    class Meta:
        model = Romaneio
        fields = '__all__'
        read_only_fields = ['ID']
    def create(self, validated_data):
        pecas_romaneio = validated_data.pop('pecas_romaneio')
        romaneio_instancia = Romaneio.objects.create(**validated_data)
        for peca in pecas_romaneio:
            Pecas.objects.create(user=romaneio_instancia,**peca)
        return romaneio_instancia

class PecasTrechoSerializer(serializers.Serializer):
    romaneio_id = serializers.IntegerField()
    ID_Trecho = serializers.IntegerField()
    Nome_Trecho = serializers.CharField()
    quantidade_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    peso_total = serializers.DecimalField(max_digits=10, decimal_places=2)

class RomaneioTrechosSerializer(serializers.ModelSerializer):
    trechos_pecas = PecasTrechoSerializer(many=True, read_only=True)
    class Meta:
        model = Romaneio
        class Meta:
            model = Romaneio
            fields = '__all__'
            read_only_fields = ['ID']

        def create(self, validated_data):
            trechos_pecas = validated_data.pop('trechos_pecas')
            romaneio_instancia = Romaneio.objects.create(**validated_data)
            for trecho in trechos_pecas:
                Pecas.objects.create(user=romaneio_instancia,**trecho)
            return romaneio_instancia
        # def get_peso_total(self, obj):
        #     return obj.Peso_Unitario * obj.Quantidade_Carregado

from django.db.models import Sum        
from django.db.models import FloatField, F
class RomaneioTrechosSerializer(serializers.ModelSerializer):
    trechos_romaneio = serializers.SerializerMethodField()

    class Meta:
        model = Romaneio
        fields = '__all__'
        read_only_fields = ['ID']

    def get_trechos_romaneio(self, obj):
        queryset = Pecas.objects.filter(romaneio_id=obj.romaneio_id).values(
            'romaneio_id', 'ID_Trecho', 'Nome_Trecho',
        ).annotate(
            quantidade_total= Sum('Quantidade_Carregado'),
            peso_total = Sum(F('Quantidade_Carregado')*F('Peso_Unitario'))
        ).order_by()

        serializer = PecasTrechoSerializer(queryset, many=True)
        return serializer.data



# class RomaneioTrechosSerializer(serializers.ModelSerializer):
#     task_extendeds = PecasTrechoSerializer(many=True)
    
#     class Meta:
#         model = Romaneio
#         fields = '__all__'