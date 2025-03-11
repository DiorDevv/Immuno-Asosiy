from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/api/', include("users.urls")),
    path('bemor/api/', include("bemor.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# from django.conf import settings
# from django.conf.urls.static import static
# from django.http import JsonResponse
# from django.urls import path, include
# from django.contrib import admin
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# from django.contrib.auth.decorators import user_passes_test
#
#
# def is_superuser(user):
#     # return user.is_superuser    # faqat superuserlar ko'ra oladi
#     return user.is_authenticated
#     # return True qilinsa istalgan user kira oladi
#
#
# # urllarninig classlarini to'g'irlab chiqing schema, swagger, redoc
#
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path('users/', include('users.urls')),
#     # path('', include('articles.urls')),
#     # path('health/', lambda _: JsonResponse({'detail': 'Healthy'}), name='health'),
#     path('schema/', user_passes_test(is_superuser)(SpectacularAPIView.as_view()), name='schema'),
#     path('swagger/', user_passes_test(is_superuser)(SpectacularSwaggerView.as_view()), name='swagger-ui'),
#     path('redoc/', user_passes_test(is_superuser)(SpectacularRedocView.as_view()), name='redoc'),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
