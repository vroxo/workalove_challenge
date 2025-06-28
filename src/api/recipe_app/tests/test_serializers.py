from uuid import uuid4

from src.api.recipe_app.serializers import (
    CreateRecipeRequestSerializer,
    DeleteRecipeRequestSerializer,
    UpdateRecipeRequestSerializer,
)


def test_when_create_recipe_request_serializer_fields_are_valid():
    serializer = CreateRecipeRequestSerializer(
        data={
            'chef_id': str(uuid4()),
            'name': 'Chef',
            'ingredients': [
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
        }
    )

    assert serializer.is_valid() is True


def test_when_create_is_active_and_description_is_not_provided_and_partial_then_do_not_add_it():
    serializer = CreateRecipeRequestSerializer(
        data={
            'chef_id': str(uuid4()),
            'name': 'Chef',
            'ingredients': [
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
        },
        partial=True,
    )

    assert serializer.is_valid() is True
    assert 'is_active' not in serializer.validated_data
    assert 'description' not in serializer.validated_data


def test_when_create_is_active_is_not_provided_and_not_partial_then_set_default_values():
    serializer = CreateRecipeRequestSerializer(
        data={
            'chef_id': str(uuid4()),
            'name': 'Chef',
            'ingredients': [
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
        },
    )
    assert serializer.is_valid() is True

    assert serializer.validated_data['is_active'] is True


def test_when_create_ingredients_is_empty_then_is_not_valid():
    serializer = CreateRecipeRequestSerializer(
        data={
            'chef_id': str(uuid4()),
            'name': 'Chef',
            'ingredients': [],
            'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
        },
    )

    assert serializer.is_valid() is False


def test_when_create_ingredients_is_not_str_then_is_not_valid():
    serializer = CreateRecipeRequestSerializer(
        data={
            'chef_id': str(uuid4()),
            'name': 'Chef',
            'ingredients': [1, 2, 3],
            'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
        },
    )

    assert serializer.is_valid() is False


def test_when_update_recipe_request_serializer_fields_are_valid():
    serializer = UpdateRecipeRequestSerializer(
        data={
            'name': 'Brigadeiro',
            'ingredients': [
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
            'is_active': True,
        }
    )

    assert serializer.is_valid() is True


def test_when_update_recipe_request_serializer_partial_fields_are_valid():
    serializer = UpdateRecipeRequestSerializer(
        data={
            'ingredients': [
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
        },
        partial=True,
    )

    assert serializer.is_valid() is True


def test_when_delete_recipe_request_serializer_fields_are_valid():
    serializer = DeleteRecipeRequestSerializer(
        data={
            'id': str(uuid4()),
        }
    )

    assert serializer.is_valid() is True
