from dataclasses import dataclass
from uuid import UUID

from src.core.chef.application.use_cases.exceptions import ChefNotFound
from src.core.chef.domain.chef_repository import ChefRepository
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository


class ListRecipeByChef:
    def __init__(self, repository: RecipeRepository, chef_repository: ChefRepository):
        self.repository = repository
        self.chef_repository = chef_repository

    @dataclass
    class Input:
        chef_id: UUID

    @dataclass
    class Output:
        data: list[Recipe]

    def execute(self, input: Input) -> Output:
        chef = self.chef_repository.get_by_id(input.chef_id)
        if chef is None:
            raise ChefNotFound('chef not found')

        recipes = self.repository.list_by_chef_id(chef.id)
        return ListRecipeByChef.Output(data=recipes)
