from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from src.api.chef_app.router import router as chefs_router
from src.api.recipe_app.router import router as recipes_router

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
    + chefs_router.urls
    + recipes_router.urls
)
