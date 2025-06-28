from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.recipe.application.use_cases.delete_recipe import DeleteRecipe
from src.core.recipe.application.use_cases.exceptions import RecipeNotFound
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import RecipeRepository


def test_delete_recipe_from_repository():
    recipe = Recipe(
        chef_id=uuid4(),
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve ao fogo médio até pegar o ponto',
    )

    mock_repository = create_autospec(RecipeRepository)
    mock_repository.get_by_id.return_value = recipe

    use_case = DeleteRecipe(mock_repository)
    use_case.execute(DeleteRecipe.Input(id=recipe.id))

    mock_repository.delete.assert_called_once_with(recipe.id)


def test_when_recipe_not_found_then_raise_exception():
    mock_repository = create_autospec(RecipeRepository)
    mock_repository.get_by_id.return_value = None

    use_case = DeleteRecipe(mock_repository)

    with pytest.raises(RecipeNotFound):
        use_case.execute(DeleteRecipe.Input(id=uuid4()))

    mock_repository.delete.assert_not_called()
