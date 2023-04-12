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


from api_carregamento.serializers import UserSerializer, GroupSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api_carregamento.models import Carregamento
from api_carregamento.serializers import CarregamentoSerializer

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

#@login_required(login_url='/admin')
class CarregamentoDetalhe(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset = Carregamento.objects.all()
    serializer_class = CarregamentoSerializer

#@login_required(login_url='/admin')
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')
    
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def carregamento_lista(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         carregamento = Carregamento.objects.all()
#         serializer = CarregamentoSerializer(carregamento, many=True)
#         return Response(serializer.data)

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