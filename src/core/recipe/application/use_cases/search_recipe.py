from dataclasses import asdict, dataclass
from typing import Optional

from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository, SearchFilterRecipe


class SearchRecipe:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    @dataclass
    class Input:
        chef_name: Optional[str] = None
        name: Optional[str] = None
        ingredient: Optional[str] = None
        description: Optional[str] = None
        preparation_method: Optional[str] = None

    @dataclass
    class Output:
        data: list[Recipe]

    def execute(self, input: Input) -> Output:
        recipes = self.repository.search(SearchFilterRecipe(**asdict(input)))
        return SearchRecipe.Output(data=recipes)
