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
        fields = ['ID','Usuario', 'Nome_Motorista','Placa_Carro', 'ID_Obra','Data_Inicio', 'Data_Final','ID_Status']
        read_only_fields = ['ID', 'Data_Final']

class RomaneioAtualizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Romaneio
        #owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['ID','Usuario', 'Nome_Motorista','Placa_Carro', 'ID_Obra','Data_Inicio', 'Data_Final','ID_Status']
        read_only_fields = ['ID', 'Data_Inicio', 'Usuario', 'Nome_Motorista','Placa_Carro', 'Data_Inicio']


# class PecasSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pecas
#         fields = '__all__'

class PecasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pecas
        fields = [
                  'ID', 
                  'Usuario',
                  'ID_TbRomaneio', 
                  'Ordem_Fabricacao',
                  'Nome_Peca',
                  'ID_Obra', 
                  'Nome_Obra', 
                  'ID_Trecho',
                  'Nome_Trecho',
                  'Quantidade_Carregado',
                  'Data',
                  ]
        read_only_fields = ['ID']
