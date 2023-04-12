from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


# Routers provide an easy way of automatically determining the URL conf.


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/', include('api_carregamento.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
# ]