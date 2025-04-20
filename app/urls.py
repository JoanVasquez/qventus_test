# 🔧 Django and DRF imports
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# 📝 Import views for parts functionality
from part.views import PartListView, PartDetailView, PartStatsView

# 📚 Configure Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Qventus API",
        default_version='v1',
        description=(
            "📦 API for managing parts and their statistics. "
            "This API allows you to retrieve, create, update, "
            "and delete parts, "
            "as well as perform other operations. "
            "as well as view the most common words in part names. "
            "as well as view the most common words in part names. "
            "as well as view the most common words in part names. "
        ),
        terms_of_service="https://www.qventus.com/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 🛣️ URL patterns configuration
urlpatterns = [
    # 👑 Admin interface
    path('admin/', admin.site.urls),

    # 🔍 API endpoints for parts
    path('api/v1/parts', PartListView.as_view()),
    path('api/v1/parts/<int:pk>', PartDetailView.as_view()),
    path('api/v1/parts/most-common-words/', PartStatsView.as_view()),

    # 📖 API Documentation URLs
    path(
        'swagger',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
