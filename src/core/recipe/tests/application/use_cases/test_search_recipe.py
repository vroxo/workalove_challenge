from dataclasses import asdict
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.recipe.application.use_cases.search_recipe import SearchRecipe
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository, SearchFilterRecipe


@pytest.fixture
def list_recipes() -> list[Recipe]:
    return [
        Recipe(
            chef_id=uuid4(),
            name='Recipe 1',
            description='Recipe 1',
            ingredients=['2 Ingredient', '2 Ingredient'],
            preparation_method='Preparation Recipe 1',
        ),
        Recipe(
            chef_id=uuid4(),
            name='Recipe 2',
            description='Recipe 2',
            ingredients=['2 Ingredient', '2 Ingredient'],
            preparation_method='Preparation Recipe 2',
        ),
        Recipe(
            chef_id=uuid4(),
            name='Recipe 3',
            description='Recipe 3',
            ingredients=['2 Ingredient', '2 Ingredient'],
            preparation_method='Preparation Recipe 3',
        ),
    ]


@pytest.fixture
def mock_repository(list_recipes: list[Recipe]) -> RecipeRepository:
    repository = create_autospec(RecipeRepository, instance=True)
    repository.search.return_value = list_recipes
    return repository


@pytest.fixture
def use_case(mock_repository: RecipeRepository) -> SearchRecipe:
    return SearchRecipe(repository=mock_repository)


def test_search_recipe(list_recipes, mock_repository, use_case):
    input = SearchRecipe.Input(
        chef_name='John', ingredient='ingredient', preparation_method='preparation'
    )

    output = use_case.execute(input)

    assert output.data == list_recipes
    mock_repository.search.assert_called_once_with(SearchFilterRecipe(**asdict(input)))
