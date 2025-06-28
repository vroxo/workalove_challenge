from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.chef.application.use_cases.exceptions import ChefNotFound
from src.core.chef.domain.chef import Chef
from src.core.chef.domain.chef_repository import ChefRepository
from src.core.recipe.application.use_cases.create_recipe import CreateRecipe
from src.core.recipe.application.use_cases.exceptions import InvalidRecipe
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository


@pytest.fixture
def chef():
    return Chef(name='Benedito')


@pytest.fixture
def mock_chef_repository(chef):
    repository = create_autospec(ChefRepository)
    repository.get_by_id.return_value = chef
    return repository


@pytest.fixture
def mock_chef_repository_empty(chef):
    repository = create_autospec(ChefRepository)
    repository.get_by_id.return_value = None
    return repository


@pytest.fixture
def mock_recipe_repository():
    return create_autospec(RecipeRepository)


@pytest.fixture
def use_case(mock_recipe_repository, mock_chef_repository):
    return CreateRecipe(repository=mock_recipe_repository, chef_repository=mock_chef_repository)


@pytest.fixture
def use_case_chef_not_found(mock_recipe_repository, mock_chef_repository_empty):
    return CreateRecipe(
        repository=mock_recipe_repository, chef_repository=mock_chef_repository_empty
    )


def test_must_be_able_to_create_recipe_with_valid_data(
    chef, mock_recipe_repository, mock_chef_repository, use_case
):
    input = CreateRecipe.Input(
        chef_id=chef.id,
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    output = use_case.execute(input)

    assert output == CreateRecipe.Output(id=output.id)

    recipe = Recipe(
        id=output.id,
        chef_id=chef.id,
        name=input.name,
        description=input.description,
        ingredients=input.ingredients,
        preparation_method=input.preparation_method,
    )
    mock_chef_repository.get_by_id.assert_called_once_with(chef.id)
    mock_recipe_repository.save.assert_called_once_with(recipe)


def test_should_be_able_to_raises_invalid_recipe_when_provided_invalid_data(use_case):
    input = CreateRecipe.Input(
        chef_id=None, name=256 * 'a', description=256 * 'a', ingredients=[], preparation_method=''
    )

    with pytest.raises(
        InvalidRecipe,
        match=(
            'chef_id cannot be none,'
            'name cannot be longer than 255,'
            'description cannot be longer than 255,'
            'preparation_method cannot be empty,ingredients cannot be empty'
        ),
    ):
        use_case.execute(input=input)


def test_should_be_able_to_raises_chef_not_found_when_provided_invalid_chef_id(
    use_case_chef_not_found,
):
    input = CreateRecipe.Input(
        chef_id=uuid4(),
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    with pytest.raises(ChefNotFound, match='chef not found'):
        use_case_chef_not_found.execute(input=input)
