from unittest.mock import create_autospec
from uuid import UUID, uuid4

import pytest

from src.core.chef.domain.chef import Chef
from src.core.chef.domain.chef_repository import ChefRepository
from src.core.recipe.application.use_cases.list_recipe_by_chef import ListRecipeByChef
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository


@pytest.fixture
def chef_id() -> UUID:
    return uuid4()


@pytest.fixture
def list_recipes(chef_id) -> list[Recipe]:
    return [
        Recipe(
            chef_id=chef_id,
            name='Recipe 1',
            description='Recipe 1',
            ingredients=['2 Ingredient', '2 Ingredient'],
            preparation_method='Preparation Recipe 1',
        ),
        Recipe(
            chef_id=chef_id,
            name='Recipe 2',
            description='Recipe 2',
            ingredients=['2 Ingredient', '2 Ingredient'],
            preparation_method='Preparation Recipe 2',
        ),
        Recipe(
            chef_id=chef_id,
            name='Recipe 3',
            description='Recipe 3',
            ingredients=['2 Ingredient', '2 Ingredient'],
            preparation_method='Preparation Recipe 3',
        ),
    ]


@pytest.fixture
def mock_chef_repository(chef_id) -> ChefRepository:
    repository = create_autospec(ChefRepository, instance=True)
    repository.get_by_id.return_value = Chef(id=chef_id, name='Chef')
    return repository


@pytest.fixture
def mock_repository(list_recipes: list[Recipe]) -> RecipeRepository:
    repository = create_autospec(RecipeRepository, instance=True)
    repository.list_by_chef_id.return_value = list_recipes
    return repository


@pytest.fixture
def use_case(
    mock_repository: RecipeRepository, mock_chef_repository: ChefRepository
) -> ListRecipeByChef:
    return ListRecipeByChef(repository=mock_repository, chef_repository=mock_chef_repository)


def test_list_recipe_by_chef(chef_id, mock_repository, mock_chef_repository, use_case):
    input = ListRecipeByChef.Input(chef_id=chef_id)
    output = use_case.execute(input=input)

    assert len(output.data) == 3
    mock_chef_repository.get_by_id.assert_called_once_with(chef_id)
    mock_repository.list_by_chef_id.assert_called_once_with(chef_id)
