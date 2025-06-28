from uuid import UUID

from django.db.models import Q

from src.api.recipe_app.models import RecipeModel
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository, SearchFilterRecipe


class DjangoORMRecipeRepository(RecipeRepository):
    def __init__(self, model: RecipeModel | None = None) -> None:
        self.model = model or RecipeModel

    def save(self, recipe: Recipe) -> None:
        recipe_model = RecipeModelMapper.to_model(recipe)
        recipe_model.save()

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def update(self, recipe: Recipe) -> None:
        self.model.objects.filter(pk=recipe.id).update(
            name=recipe.name,
            description=recipe.description,
            ingredients=recipe.ingredients,
            preparation_method=recipe.preparation_method,
            is_active=recipe.is_active,
        )

    def get_by_id(self, id: UUID) -> Recipe | None:
        try:
            recipe_model = self.model.objects.get(id=id)
            return RecipeModelMapper.to_entity(recipe_model)
        except self.model.DoesNotExist:
            return None

    def search(self, filter: SearchFilterRecipe):
        query = Q()

        if filter.chef_name is not None:
            query &= Q(chef__name__icontains=filter.chef_name)

        if filter.name is not None:
            query &= Q(name__icontains=filter.name)

        if filter.description is not None:
            query &= Q(description__icontains=filter.description)

        if filter.ingredient is not None:
            query &= Q(ingredients__icontains=filter.ingredient)

        if filter.preparation_method is not None:
            query &= Q(preparation_method__icontains=filter.preparation_method)

        recipes_model = RecipeModel.objects.filter(query).select_related('chef')

        return [RecipeModelMapper.to_entity(recipe_model) for recipe_model in recipes_model]

    def list_by_chef_id(self, chef_id: UUID) -> list[Recipe]:
        recipes_model = RecipeModel.objects.filter(Q(chef_id=chef_id)).select_related('chef')

        return [RecipeModelMapper.to_entity(recipe_model) for recipe_model in recipes_model]


class RecipeModelMapper:
    @staticmethod
    def to_entity(model: RecipeModel) -> Recipe:
        entity = Recipe(
            id=model.id,
            chef_id=model.chef.id,
            name=model.name,
            description=model.description,
            ingredients=model.ingredients,
            preparation_method=model.preparation_method,
            is_active=model.is_active,
        )
        entity.created_at = model.created_at
        entity.updated_at = model.updated_at

        return entity

    @staticmethod
    def to_model(entity: Recipe) -> RecipeModel:
        model = RecipeModel(
            id=entity.id,
            chef_id=entity.chef_id,
            name=entity.name,
            description=entity.description,
            ingredients=entity.ingredients,
            preparation_method=entity.preparation_method,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        model.chef_id = entity.chef_id
        return model
