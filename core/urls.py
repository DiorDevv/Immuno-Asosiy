from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/api/', include("users.urls")),
    path('bemor/api/', include("bemor.urls")),
    path('dori/api/', include('dori.urls')),
    path('shifokor/api/', include('shifokor.urls')),
]
