from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.recipe.application.use_cases.exceptions import InvalidRecipe, RecipeNotFound
from src.core.recipe.domain.recipe_repository import RecipeRepository


class UpdateRecipe:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: Optional[str] = None
        ingredients: Optional[list[str]] = None
        preparation_method: Optional[str] = None
        description: Optional[str] = None
        is_active: Optional[bool] = None

    def execute(self, input: Input) -> None:
        try:
            recipe = self.repository.get_by_id(id=input.id)

            if not recipe:
                raise RecipeNotFound('recipe not found')

            current_name = recipe.name
            current_description = recipe.description
            current_ingredients = recipe.ingredients
            current_preparation_method = recipe.preparation_method

            if input.name:
                current_name = input.name

            if input.description:
                current_description = input.description

            if input.ingredients is not None:
                current_ingredients = input.ingredients

            if input.preparation_method:
                current_preparation_method = input.preparation_method

            if input.is_active is True:
                recipe.activate()

            if input.is_active is False:
                recipe.deactivate()

            recipe.update(
                name=current_name,
                description=current_description,
                ingredients=current_ingredients,
                preparation_method=current_preparation_method,
            )

            self.repository.update(recipe=recipe)

        except ValueError as error:
            raise InvalidRecipe(error)
