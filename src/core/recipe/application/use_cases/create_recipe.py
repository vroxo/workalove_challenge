from dataclasses import asdict, dataclass
from typing import Optional
from uuid import UUID

from src.core.chef.application.use_cases.exceptions import ChefNotFound
from src.core.chef.domain.chef_repository import ChefRepository
from src.core.recipe.application.use_cases.exceptions import InvalidRecipe
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository


class CreateRecipe:
    def __init__(self, repository: RecipeRepository, chef_repository: ChefRepository):
        self.repository = repository
        self.chef_repository = chef_repository

    @dataclass
    class Input:
        chef_id: UUID
        name: str
        ingredients: list[str]
        preparation_method: str
        description: Optional[str] = None
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            chef = self.chef_repository.get_by_id(id=input.chef_id)

            if not chef:
                raise ChefNotFound('chef not found')

            recipe = Recipe(**asdict(input))
            self.repository.save(recipe)

            return CreateRecipe.Output(id=recipe.id)
        except ValueError as error:
            raise InvalidRecipe(error)
