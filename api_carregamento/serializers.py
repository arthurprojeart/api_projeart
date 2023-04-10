from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api_carregamento.models import Carregamento


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

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     nome = serializers.CharField(max_length=100, blank=True, default='')
#     carregamento = serializers.CharField(max_length=100, blank=True, default='')
#     pecas = serializers.CharField(max_length=100, blank=True, default='')

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Carregamento.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.nome = validated_data.get('nome', instance.nome)
#         instance.carregamento = validated_data.get('carregamento', instance.carregamento)
#         instance.pecas = validated_data.get('pecas', instance.pecas)
#         instance.save()
#         return instance