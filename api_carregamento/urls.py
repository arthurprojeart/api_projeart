from django.urls import include, path
from rest_framework import routers
from api_carregamento import views
from rest_framework.urlpatterns import format_suffix_patterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    #path('carregamentos/', views.CarregamentoLista.as_view()),
    #path('carregamentos/<int:pk>/', views.CarregamentoDetalhe.as_view()),
    path('romaneios/',views.RomaneioLista.as_view()),
    path('romaneios/<int:pk>/',views.AtualizaRomaneio.as_view()),
    path('romaneios/<int:pk>/delete',views.DeleteRomaneio.as_view()),
    path('romaneios/delete/',views.delete_romaneio),
    path('romaneios/pecas/',views.CarregarPecas.as_view()),

    #path('romaneios/<int:pk>/peca',views.AtualizaRomaneio.as_view()),
    path('obras/',views.obras_lista),
    path('trechos/',views.trechos_lista),
    path('pecas/detalhe/',views.peca_detalhe),
    path('pecas/<int:id_romaneio>',views.PecasCarregadas.as_view()),
    path('pecas/',views.PecasCarregadas.as_view()),
    #path('users/', views.UserList.as_view()),
    #path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)