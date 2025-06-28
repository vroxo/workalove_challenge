from rest_framework.routers import DefaultRouter

from src.api.recipe_app.views import RecipeViewSet

router = DefaultRouter()
router.register(r'api/recipes', RecipeViewSet, basename='recipes')
