from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/v1/',include('djoser.urls')),
    path('api/v1/',include('djoser.urls.authtoken')),
    path('api/v1/',include('core.api.urls')),
    
    #custom registration app
     path('auth/', include('users.urls')),
     path('api/v1/',include('profiles.api.urls')),
     path('api/v1/',include('cooperators.api.urls')),
     
    #documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
