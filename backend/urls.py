"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from backend import settings

API_VERSION = "v1"
schema_view = get_schema_view(
    openapi.Info(
        title="X-Project API",
        default_version=f"{API_VERSION}",
        description="API of the X-Project backend project",
        contact=openapi.Contact(
            email="edghimakoll@gmail.com",
            name="Edmond Makolle",
        ),
    ),
)
START_URL = f"api/{API_VERSION}"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{START_URL}/", include("endpoints.auth.urls")),
    path(f"{START_URL}/services/", include("endpoints.services.urls")),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("", schema_view.with_ui("swagger", cache_timeout=0)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
