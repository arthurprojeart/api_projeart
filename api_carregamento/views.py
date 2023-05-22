from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from api_carregamento.permissions import IsOwnerOrReadOnly
from rest_framework import generics, status
from django.db.models import Q
from api_carregamento.models import  Romaneio, Pecas, Ordens, LeiturasCarregamento #Carregamento,
from api_carregamento.serializers import RomaneioSerializer, PecasLeiturasRecebimentoSerializer,LeituraRecebimentoSerializer,LeituraSerializer, PecasSerializer, PecasLeiturasCarregamentoSerializer, OrdensSerializer, RomaneioAtualizaSerializer, PecasRecebimentoSerializer, RecebimentoSerializer, PecasTrechoSerializer, RomaneioTrechosSerializer, PecasLeiturasSerializer, LeiturasCarregamentoSerializer #CarregamentoSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import dw_connect, db_connect
from django.db.models import Prefetch

#Lista Geral de Obras
#ENDPOINT 1 [GET]
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obras_lista(request, format=None):
    if request.method == 'GET':
        obras = dw_connect.query_obras()
        return Response(obras)

#Lista dos Trechos por Obra Parâmetro ID_Obra
#ENDPOINT 2 [GET]
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trechos_lista(request, format=None):
    obra_id = request.GET['obra_id']
    if request.method == 'GET':
        trechos = dw_connect.query_trechos(obra_id)
        return Response(trechos)

#Lista para buscar Numero de Ordem ou Nome do Objeto
#ENDPOINT 3 [GET]
class PegarPecas(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        peca = dw_connect.query_get_peca(request.GET.get('ordem_ou_nome'))
        return HttpResponse(peca, status=status.HTTP_200_OK)

# Lista dos Carregamentos com Parâmetros de ID_Obra, ID_Trecho e ID_Status
# ENDPOINT 4[GET], 5[POST]
class Romaneios(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # ordens = Ordens.objects.prefetch_related('Leituras_Carregamento')
        # for ordem in ordens:
        #     print(ordem.Quantidade_Carregada)

        if request.GET.get('ID_Obra') == '':
            ID_Obra = None
        else:
            ID_Obra = request.GET.get('ID_Obra')
        if request.GET.get('ID_Status') == '':     
            ID_Status = None
        else:
            ID_Status = request.GET.get('ID_Status')
        if ID_Status is None and ID_Obra is not None:
            queryset = Romaneio.objects.filter(ID_Obra=ID_Obra)
        elif ID_Obra is None and ID_Status is not None:
            queryset = Romaneio.objects.filter(ID_Status=ID_Status)
        elif ID_Obra is not None and ID_Status is not None:
            queryset = Romaneio.objects.filter(Q(ID_Obra=ID_Obra) & Q(ID_Status=ID_Status))
        else:
            queryset = Romaneio.objects.all()
        serializer = RomaneioTrechosSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = RomaneioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ENDPOINT 6[PUT], 8[DELETE]
class RomaneioAtualiza(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        my_data = Romaneio.objects.get(pk=pk)
        serializer = RomaneioAtualizaSerializer(my_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        my_data = Romaneio.objects.get(pk=pk)
        my_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#LISTA COM PEÇAS DE UM ROMANEIO
#ENDPOINT 7[POST], 9[GET], 10[DELETE]
class PecasRomaneio(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # Parâmetro - romaneio_id
    def get(self, request, format=None):
        queryset = Ordens.objects.filter(romaneio_id=request.GET.get('romaneio_id'))
        serializer = PecasLeiturasCarregamentoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Parâmetros JSON - Ordem_Fabricacao, romaneio_id, Usuario, Quantidade_Carregado    
    def post(self, request, format=None):
        peca = dw_connect.query_get_ordem(request.data.get('Ordem_Fabricacao'))
        peca['romaneio_id'] = request.data.get('romaneio_id')
        peca['Usuario'] = request.data.get('Usuario')
        peca['Quantidade_Carregada'] = request.data.get('Quantidade_Carregada')

        query_teste = Ordens.objects.filter(Ordem_Fabricacao=request.data.get('Ordem_Fabricacao')).exists()
        # print(query_teste)
        
        # print(serializer_leituras)
        if query_teste:
            pk = request.data.get('Ordem_Fabricacao')
            instance = Ordens.objects.get(pk=pk)
            serializer_ordens = OrdensSerializer(instance, peca)
        else:
            serializer_ordens = OrdensSerializer(data=peca)
        # print(serializer_ordens)
        serializer_leituras = LeiturasCarregamentoSerializer(data=peca)
        
        if serializer_ordens.is_valid():
            serializer_ordens.save()
            if serializer_leituras.is_valid():
                serializer_leituras.save()
            return Response({'Ordens': serializer_ordens.data, 'LeiturasCarregamento': serializer_leituras.data}, status=status.HTTP_201_CREATED)
        return Response(serializer_leituras.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        #my_data = Pecas.objects.get(pk=pk)
        dados = request.data
        lista_excluir = dados['Leitura_ID']
        for leitura in lista_excluir:   
            queryset = LeiturasCarregamento.objects.filter(Leitura_ID=leitura)
            queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#LISTA DE RECEBIMENTO
#ENDPOINT 11[GET] 12[POST]
class PecasRecebimento(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # EP 11
    def get(self, request, format=None):
        queryset = Romaneio.objects.filter(ID_Obra=request.GET.get('ID_Obra'))
        # queryset = Ordens.objects.select_related('LeiturasRecebimento').all()
        serializer = PecasLeiturasRecebimentoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # EP 12
    def post(self, request, format=None):
        serializer_recebimento = LeituraRecebimentoSerializer(data=request.data)
        if serializer_recebimento.is_valid():
            serializer_recebimento.save()
            return Response(serializer_recebimento.data, status=status.HTTP_201_CREATED)
        return Response(serializer_recebimento.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        my_data = Pecas.objects.get(pk=pk)
        serializer = RecebimentoSerializer(my_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Sum
from django.db.models import F

class PecasTeste(APIView):

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # Parâmetros JSON - Ordem_Fabricacao, romaneio_id, Usuario, Quantidade_Carregado    
    def post(self, request, format=None):
        
        peca = dw_connect.query_get_ordem(request.data.get('Ordem_Fabricacao'))
        peca['romaneio_id'] = request.data.get('romaneio_id')
        peca['Usuario'] = request.data.get('Usuario')
        # peca['Quantidade_Produzida'] = request.data.get('Quantidade_Produzida')
        peca['Quantidade_Carregada'] = request.data.get('Quantidade_Carregada')
        # peca['Quantidade_Projeto'] = request.data.get('Quantidade_Projeto')


        query_teste = Ordens.objects.filter(Ordem_Fabricacao=request.data.get('Ordem_Fabricacao')).exists()
        serializer_leituras = LeiturasCarregamentoSerializer(data=peca)

        serializer_ordens = OrdensSerializer(data=peca)

        if serializer_ordens.is_valid() :
            serializer_ordens.save()
            return Response(serializer_ordens.data, status=status.HTTP_201_CREATED)
        return Response(serializer_ordens.errors, status=status.HTTP_400_BAD_REQUEST)

  