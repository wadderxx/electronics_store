from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def home(request):
    return JsonResponse({
        "message": "Electronics Store API ishlayapti!"
    })


urlpatterns = [
    # Root endpoint
    path('', home),

    # Django Admin
    path('admin/', admin.site.urls),

    # Application APIs
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/cart/', include('cart.urls')),

    # OpenAPI sxemasi
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),

    # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),

    # ReDoc
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

# Media files — faqat DEBUG rejimida
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )