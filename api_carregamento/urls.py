from django.urls import include, path
from rest_framework import routers
from api_carregamento import views
from rest_framework.urlpatterns import format_suffix_patterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('carregamentos/', views.CarregamentoLista.as_view()),
    path('carregamentos/<int:pk>/', views.CarregamentoDetalhe.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)