from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api_carregamento.models import Carregamento, Romaneio


class UserSerializer(serializers.ModelSerializer):
    carregamento = serializers.PrimaryKeyRelatedField(many=True, queryset=Carregamento.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'carregamento']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CarregamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carregamento
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['id', 'owner','nome', 'carregamento', 'pecas']

class RomaneioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Romaneio
        fields = ['usuario', 'nome_motorista','placa_carro', 'data_inicio', 'data_final','id_status']