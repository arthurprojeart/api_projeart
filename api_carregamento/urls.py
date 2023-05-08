from django.urls import include, path
from rest_framework import routers
from api_carregamento import views
from rest_framework.urlpatterns import format_suffix_patterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    # ENDPOINT 1[GET]
    path('obras/',views.obras_lista),
    # ENDPOINT 2[GET]
    path('trechos/',views.trechos_lista),
    # ENDPOINT 3[GET]
    path('pecas/detalhe/',views.PegarPecas.as_view()),
    # ENDPOINT 4[GET] , ENDPOINT 5[POST]
    path('romaneios/',views.RomaneioLista.as_view()),
    # ENDPOINT 6[PUT] , ENDPOINT 8[DELETE]
    path('romaneios/<int:pk>/',views.RomaneioAtualiza.as_view()),
    # ENDPOINT 7[POST], 9[GET]
    path('pecas/',views.PecasRomaneio.as_view()),
    # ENDPOINT 10[DELETE]
    path('pecas/<int:pk>/',views.PecasRomaneio.as_view()),
    # ENPOINT 11[GET], 12[POST]
    path('recebimento/',views.PecasRecebimento.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)