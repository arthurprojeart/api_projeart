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
from api_carregamento.models import  Romaneio, Pecas #Carregamento,
from api_carregamento.serializers import RomaneioSerializer, PecasSerializer, RomaneioAtualizaSerializer, PecasRecebimentoSerializer, RecebimentoSerializer, PecasTrechoSerializer, RomaneioTrechosSerializer #CarregamentoSerializer, UserSerializer

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
        return Response(peca, status=status.HTTP_200_OK)

# Lista dos Romaneios com Parâmetros de ID_Obra, ID_Trecho e ID_Status
# ENDPOINT 4[GET], 5[POST]
class RomaneioLista(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        if request.GET.get('ID_Obra') is not None:
            ID_Obra = request.GET.get('ID_Obra')
            ID_Status = request.GET.get('ID_Status')
            if len(ID_Obra)>0:
                ID_Obra = request.GET.get('ID_Obra')
            else:
                ID_Obra  = 0
            if len(ID_Status)>0:
                ID_Status = request.GET.get('ID_Status')
            else:
                ID_Status = ''
            print(ID_Obra, ID_Status)
            if ID_Obra != 0 or ID_Status != '':
                print('entrou')
                queryset = Romaneio.objects.filter(Q(ID_Obra=ID_Obra) | Q(ID_Status=ID_Status))
            else:
                queryset = Romaneio.objects.all()
            serializer = RomaneioTrechosSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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

# ENDPOINT 7[POST], 9[GET]
class PecasLista(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Pecas.objects.all()
        serializer = PecasSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#LISTA COM PEÇAS DE UM ROMANEIO
#ENDPOINT 7[POST], 9[GET], 10[DELETE]
class PecasRomaneio(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # Parâmetro - romaneio_id
    def get(self, request,format=None):
        querypecas = Pecas.objects.filter(romaneio_id=request.GET.get('romaneio_id'))
        serializer = PecasSerializer(querypecas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Parâmetros JSON - Ordem_Fabricacao, romaneio_id, Usuario, Quantidade_Carregado    
    def post(self, request, format=None):
        peca = dw_connect.query_get_ordem(request.data.get('Ordem_Fabricacao'))
        peca['romaneio_id'] = request.data.get('romaneio_id')
        peca['Usuario'] = request.data.get('Usuario')
        peca['Quantidade_Carregado'] = request.data.get('Quantidade_Carregado')
        serializer_pecas = PecasSerializer(data=peca)

        if serializer_pecas.is_valid():
            pecas = serializer_pecas.save()
            return Response(serializer_pecas.data, status=status.HTTP_201_CREATED)
        return Response(serializer_pecas.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        my_data = Pecas.objects.get(pk=pk)
        my_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PecasRecebimento(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        queryset = Romaneio.objects.filter(ID_Obra=request.GET.get('ID_Obra'))
        serializer = PecasRecebimentoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        my_data = Pecas.objects.get(pk=pk)
        serializer = RecebimentoSerializer(my_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Sum
class PecasTeste(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Romaneio.objects.filter(romaneio_id=request.GET.get('romaneio_id'))
        serializer = RomaneioTrechosSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class PecasTeste(generics.ListAPIView):
#     serializer_class = RomaneioTrechosSerializer

#     def get_queryset(self):
#         queryset = Romaneio.objects.filter(romaneio_id=1)
#         return queryset.prefetch_related('romaneio_id')