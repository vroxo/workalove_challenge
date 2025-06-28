from uuid import UUID, uuid4

import pytest

from src.core.recipe.domain.recipe import Recipe


@pytest.fixture
def chef_id():
    return uuid4()


@pytest.fixture
def recipe(chef_id):
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


def test_must_be_able_to_create_recipe_with_valid_data(chef_id, recipe):
    assert isinstance(recipe.id, UUID)
    assert recipe.chef_id == chef_id
    assert recipe.name == 'Brigadeiro'
    assert recipe.description == 'Receita de Brigadeiro'
    assert recipe.ingredients == [
        '1 Lata de Leite Condensado',
        '2 Colheres de Sopa de Achocolatado',
        '1 Colher de Chá de Manteiga',
    ]
    assert recipe.preparation_method == 'Misture tudo e leve al fogo médio até pegar o ponto'
    assert recipe.is_active is True


def test_should_be_able_to_raises_value_error_when_invalid_data(chef_id):
    with pytest.raises(ValueError, match='name cannot be longer than 255'):
        Recipe(
            chef_id=chef_id,
            name=256 * 'B',
            description='Receita de Brigadeiro',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
        )

    with pytest.raises(ValueError, match='description cannot be longer than 255'):
        Recipe(
            chef_id=chef_id,
            name='Brigadeiro',
            description=256 * 'B',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
        )

    with pytest.raises(ValueError, match='name cannot be empty'):
        Recipe(
            chef_id=chef_id,
            name='',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
        )

    with pytest.raises(ValueError, match='chef_id cannot be none'):
        Recipe(
            chef_id=None,
            name='Brigadeiro',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
        )

    with pytest.raises(ValueError, match='ingredients cannot be empty'):
        Recipe(
            chef_id=chef_id,
            name='Brigadeiro',
            ingredients=[],
            preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
        )

    with pytest.raises(ValueError, match='preparation_method cannot be empty'):
        Recipe(
            chef_id=chef_id,
            name='Brigadeiro',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method='',
        )


def test_should_be_able_to_update_recipe_with_valid_data(recipe):
    recipe.update(
        name='Gelatina',
        description='Gelatina',
        ingredients=['Água quente', 'Gelatina em pó'],
        preparation_method='Ferva a água e jogue a gelatina e mexa',
    )

    assert recipe.name == 'Gelatina'
    assert recipe.description == 'Gelatina'
    assert recipe.ingredients == ['Água quente', 'Gelatina em pó']
    assert recipe.preparation_method == 'Ferva a água e jogue a gelatina e mexa'


def test_should_be_able_to_raises_value_error_when_invalid_name(recipe):
    with pytest.raises(
        ValueError,
        match='name cannot be empty,preparation_method cannot be empty,ingredients cannot be empty',
    ):
        recipe.update(name='', description=256 * 'a', ingredients=[], preparation_method='')


def test_should_be_able_to_activate_recipe_when_is_deactivated(recipe):
    recipe.activate()
    assert recipe.is_active is True


def test_should_be_able_to_activate_recipe_when_is_activated(recipe):
    recipe.activate()
    assert recipe.is_active is True


def test_should_be_able_to_deactivate_recipe_when_is_activated(recipe):
    recipe.deactivate()
    assert recipe.is_active is False


def test_should_be_able_to_deactivate_recipe_when_is_deactivated(recipe):
    recipe.deactivate()
    assert recipe.is_active is False


def test_should_be_able_to_create_recipe_when_provided_id():
    recipe_id = uuid4()
    recipe = Recipe(
        id=recipe_id,
        chef_id=chef_id,
        name='Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    assert recipe.id == recipe_id


def test_should_be_able_to_create_recipe_activated_when_not_provided_is_active():
    recipe = Recipe(
        chef_id=chef_id,
        name='Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    assert recipe.is_active is True
