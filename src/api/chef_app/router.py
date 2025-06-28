from rest_framework.routers import DefaultRouter

from src.api.chef_app.views import ChefViewSet

router = DefaultRouter()
router.register(r'api/chefs', ChefViewSet, basename='chefs')
