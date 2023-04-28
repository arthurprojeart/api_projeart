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

from api_carregamento.models import  Romaneio, Pecas #Carregamento,
from api_carregamento.serializers import RomaneioSerializer, PecasSerializer, RomaneioAtualizaSerializer #CarregamentoSerializer, UserSerializer

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import dw_connect, db_connect

class RomaneioLista(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Romaneio.objects.all()
    serializer_class = RomaneioSerializer
    def perform_create(self, serializer):
        serializer.save()

class AtualizaRomaneio(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Romaneio.objects.all()
    serializer_class = RomaneioAtualizaSerializer
    lookup_field = 'pk'
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Sucesso!!"})
        else:
            return Response({"message": "failed", "details": serializer.errors})

class DeleteRomaneio(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Romaneio.objects.all()
    serializer_class = RomaneioSerializer
    lookup_field = 'pk'
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_romaneio(request, format=None):
    id_romaneio = request.GET['ID']
    if request.method == 'DELETE':
        db_connect.query_delete_pecas(id_romaneio)
        db_connect.query_delete_romaneio(id_romaneio)
        return Response('Romaneio deletado!')

class PecasCarregadas(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pecas.objects.all()
    serializer_class = PecasSerializer

    def perform_create(self, serializer):
        serializer.save()

class CarregarPecas(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Pecas.objects.all()
        serializer = PecasSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        peca = dw_connect.query_get_ordem(request.data.get('Ordem_Fabricacao'))
        peca['ID_TbRomaneio'] = request.data.get('ID_TbRomaneio')
        peca['Usuario'] = request.data.get('Usuario')
        peca['Quantidade_Carregado'] = request.data.get('Quantidade_Carregado')
        serializer_pecas = PecasSerializer(data=peca)

        if serializer_pecas.is_valid():
            pecas = serializer_pecas.save()
            return Response(PecasSerializer(pecas).data, status=status.HTTP_201_CREATED)
        return Response(serializer_pecas.errors, status=status.HTTP_400_BAD_REQUEST)

class ObrasLista(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    dw_connect.query_obras()
    #queryset = get_queryset()
    def perform_create(self, serializer):
        serializer.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obras_lista(request, format=None):
    if request.method == 'GET':
        obras = dw_connect.query_obras()
        return Response(obras)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trechos_lista(request, format=None):
    obra_id = request.GET['obra_id']
    if request.method == 'GET':
        trechos = dw_connect.query_trechos(obra_id)
        return Response(trechos)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def peca_detalhe(request, format=None):
    peca_id = request.GET['ordem_ou_nome']
    if request.method == 'GET':
        peca = dw_connect.query_get_peca(peca_id)
        
        return Response(peca)


