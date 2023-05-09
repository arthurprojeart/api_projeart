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
                  'Nome_Motorista',
                  'Placa_Carro', 
                  'ID_Obra',
                  'Data_Inicio', 
                  'Usuario_Inicio',
                  'Data_Final',
                  'Usuario_Final',
                  'ID_Status']
        read_only_fields = ['ID', 'ID_Obra','Data_Inicio', 'Usuario_Inicio', 'Nome_Motorista','Placa_Carro']


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

