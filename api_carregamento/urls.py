from django.urls import include, path
from rest_framework import routers
from api_carregamento import views
from rest_framework.urlpatterns import format_suffix_patterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    
    path('obras/',views.obras_lista),
    path('trechos/',views.trechos_lista),
    path('romaneios/',views.RomaneioLista.as_view()),
    path('romaneios/<int:pk>/',views.RomaneioAtualiza.as_view()),
    
    #path('pecas/',views.PecasLista.as_view()),

    path('pecas/',views.PecasRomaneio.as_view()),
    path('pecas/<int:pk>/',views.PecasRomaneio.as_view()),

    path('recebimento/',views.PecasRecebimento.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)