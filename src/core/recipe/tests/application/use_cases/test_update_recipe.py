from unittest.mock import create_autospec
from uuid import UUID, uuid4

import pytest

from src.core.recipe.application.use_cases.exceptions import InvalidRecipe, RecipeNotFound
from src.core.recipe.application.use_cases.update_recipe import UpdateRecipe
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository


@pytest.fixture
def chef_id() -> UUID:
    return uuid4()


@pytest.fixture
def recipe(chef_id: UUID) -> Recipe:
    return Recipe(
        chef_id=chef_id,
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )


@pytest.fixture
def mock_repository(recipe: Recipe) -> RecipeRepository:
    repository = create_autospec(RecipeRepository, instance=True)
    repository.get_by_id.return_value = recipe
    return repository


def test_update_recipe_name(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(id=recipe.id, name='Update Name')
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.name == 'Update Name'
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_description(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(id=recipe.id, description='Update description')
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.description == 'Update description'
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_ingredients(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(id=recipe.id, ingredients=['Update ingredients'])
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.ingredients == ['Update ingredients']
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_preparation_method(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(id=recipe.id, preparation_method='Update preparation_method')
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.preparation_method == 'Update preparation_method'
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_provided_all_valid_values(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(
        id=recipe.id,
        name='Update Name',
        preparation_method='Update preparation_method',
        description='Update description',
        ingredients=['Update description'],
        is_active=False,
    )
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.name == 'Update Name'
    assert recipe.description == 'Update description'
    assert recipe.ingredients == ['Update description']
    assert recipe.preparation_method == 'Update preparation_method'
    assert recipe.is_active is False
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_activate(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(id=recipe.id, is_active=True)
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.is_active is True
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_deactivate(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(id=recipe.id, is_active=False)
    use_case = UpdateRecipe(mock_repository)
    use_case.execute(input)

    assert recipe.is_active is False
    mock_repository.update.assert_called_once_with(recipe)


def test_update_recipe_provided_all_invalid_values(
    mock_repository: RecipeRepository,
    recipe: Recipe,
):
    input = UpdateRecipe.Input(
        id=recipe.id,
        name=256 * 'N',
        description=256 * 'N',
        ingredients=[],
    )
    use_case = UpdateRecipe(mock_repository)

    with pytest.raises(
        InvalidRecipe,
        match=(
            'name cannot be longer than 255,'
            'description cannot be longer than 255,'
            'ingredients cannot be empty'
        ),
    ):
        use_case.execute(input)


def test_cannot_update_recipe_when_recipe_not_found():
    input = UpdateRecipe.Input(
        id=uuid4(),
        name='Update Name',
        preparation_method='Update preparation_method',
        description='Update description',
        ingredients=['Update description'],
    )
    repository = create_autospec(RecipeRepository, instance=True)
    repository.get_by_id.return_value = None

    use_case = UpdateRecipe(repository)

    with pytest.raises(RecipeNotFound, match='recipe not found'):
        use_case.execute(input)
