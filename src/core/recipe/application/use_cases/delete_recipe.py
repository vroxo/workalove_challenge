from dataclasses import dataclass
from uuid import UUID

from src.core.recipe.application.use_cases.exceptions import RecipeNotFound
from src.core.recipe.domain.recipe_repository import RecipeRepository


class DeleteRecipe:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        recipe = self.repository.get_by_id(input.id)

        if recipe is None:
            raise RecipeNotFound('recipe not found')

        self.repository.delete(recipe.id)
