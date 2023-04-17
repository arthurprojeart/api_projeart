from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from api_carregamento.permissions import IsOwnerOrReadOnly
from rest_framework import generics

from json import loads, dumps
from api_carregamento.serializers import UserSerializer, GroupSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api_carregamento.models import Carregamento, Romaneio
from api_carregamento.serializers import CarregamentoSerializer, RomaneioSerializer

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#@login_required(login_url='/admin')
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#@login_required(login_url='/admin')
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#@login_required(login_url='admin/')
class CarregamentoLista(generics.ListCreateAPIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Carregamento.objects.all()
    serializer_class = CarregamentoSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RomaneioLista(generics.ListCreateAPIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Romaneio.objects.all()
    serializer_class = RomaneioSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

import dw_connect
from rest_framework.decorators import api_view
from rest_framework.response import Response

class ObrasLista(generics.ListCreateAPIView):
    
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    dw_connect.query_obras()
    #queryset = get_queryset()
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CarregamentoDetalhe(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset = Carregamento.objects.all()
    serializer_class = CarregamentoSerializer

#@login_required(login_url='/admin')
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

import dw_connect    
@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@permission_classes([IsAuthenticated])
def obras_lista(request, format=None):

    if request.method == 'GET':
        obras = dw_connect.query_obras()
        #obras.replace("\",'')
        return Response(obras)

@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@permission_classes([IsAuthenticated])
def trechos_lista(request, format=None):

    obra_id = request.GET['obra_id']
    if request.method == 'GET':
        trechos = dw_connect.query_trechos(obra_id)
        
        return Response(trechos)

@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@permission_classes([IsAuthenticated])
def peca_detalhe(request, format=None):

    peca_id = request.GET['ordem_ou_nome']

    if request.method == 'GET':
        peca = dw_connect.query_get_peca(peca_id)
        
        return Response(peca)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = CarregamentoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def carregamento_detalhe(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         carregamento = Carregamento.objects.get(pk=pk)
#     except Carregamento.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = CarregamentoSerializer(carregamento)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = CarregamentoSerializer(carregamento, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         carregamento.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)